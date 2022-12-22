import logging
import os
import pickle
import json
import pandas as pd
from analyticexecution.analytic_base import AnalyticBase
from analyticexecution.analytic_model import *
from analyticexecution.analytic_model import DataPayload, AnalyticOutputPayload
from analyticexecution.model_paths import ModelPaths

from config.analytic_config import AnalyticConfig
from methods import available_methods
from pipeline.train_pipeline import get_data_pipe
from utils import get_parameter, construct_output_threshold, silent_numerify, simple_voting, simple_mean_of_cfs
from utils import missing_val_handling, test_plot_anomalies, str2bool, construct_output_score, fetch_allowed_tag_list

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
logger = logging.getLogger('execution-subprocess')


class Analytic(AnalyticBase):
    VERSION = 1.1
    logger.info('VERSION:{}'.format(VERSION))

    def __init__(self):
        super(Analytic, self).__init__()

    def initialize(self):
        logger.info('initialise called')
        pass

    def load_models(self):
        try:
            pass
        except Exception as e:
            self.log(e)
            return None

    def score(self, data: DataPayload) -> AnalyticOutputPayload:

        allowed_tags = fetch_allowed_tag_list(data)
        norm_flag = str2bool(data.parameters.get('norm_flag', 'True'))
        threshold = get_parameter(name='threshold', var_type=float, data=data, default=1)
        raise_alert_count = get_parameter(name='raise_alert_count', var_type=int, data=data, default=1)
        trained_model_path = data.parameters.get('trained_model_path', None)
        local_train_score = str2bool(data.parameters.get('local_train_score', 'False'))
        if not trained_model_path:
            trained_model_path = ModelPaths.trained_artifacts_pickled_file_path

        try:
            model_name = data.model_name
        except:
            model_name = 'Unnamed model'

        logger.info(model_name + ':score called')
        logger.info('data: {}'.format(data))
        logger.info('data parameters: {}'.format(data.parameters))
        logger.info('data: {}'.format(data.df))
        if allowed_tags is not None:
            data.df = data.df[allowed_tags]
        data.df = missing_val_handling(data.df, model='interpolate', method='linear')
        try:
            # Check if debug mode
            debug = str2bool(get_parameter(name='debug', var_type=str, data=data))
            # Get methods to train and check validity
            methods = self.get_methods(data)
            if methods is None:
                logger.error(model_name + ':No methods are specified . Aborting scoring routine.')
                return AnalyticOutputPayload([])

            agreement_factor = get_parameter(name='agreement_factor', var_type=float, data=data)

            # Get available models and check if they exist for all methods.
            try:
                with open(trained_model_path, 'rb') as f:
                    model_dict = pickle.load(f)
                models_keys = model_dict.keys()
                logger.info('models keys: {}'.format(models_keys))
            except Exception as e:
                logger.exception('Error: {}'.format(e))
                self.log(model_name + ':Could not find or load the model file. Aborting scoring routine.')
                self.log(e)
                return AnalyticOutputPayload([])

            if any([x['name'] for x in methods if x['name'] not in models_keys]):
                logger.error(model_name + ':One or more models could not be found for the specified methods. '
                                          'Aborting scoring routine.')
                return AnalyticOutputPayload([])

            method_labels = None
            method_scores = None
            method_cfs = []

            for method in methods:
                pkl_dict = model_dict[method['name']]

                data_pipeline = pkl_dict['data-pipe']
                clf = pkl_dict['model']
                method_df = pd.DataFrame(data=data_pipeline.transform(data.df),
                                         index=list(data.df.index),
                                         columns=allowed_tags)
                logger.info('data df: {}'.format(data.df.shape))
                logger.info('method df: {}'.format(method_df))
                logger.info('data df index: {}'.format(data.df.index))

                test_labels = clf.predict(np.array(method_df.values))
                if norm_flag:
                    test_labels = np.ones_like(test_labels)

                test_scores = (clf.detector.decision_function(
                    np.array(method_df.values)) * test_labels) / clf.detector.threshold_

                logger.info('Labels & scores {}, {}'.format(test_labels, test_scores))
                df_cfs = clf.calculate_contributing_factors(method_df, test_labels)
                logger.info('Calculated CF {}'.format(df_cfs))

                if method_labels is None and method_scores is None:
                    method_labels = test_labels
                    method_scores = test_scores
                elif method_labels is None or method_scores is None:
                    raise Exception(model_name + ':ERROR - method_labels and method_scores are out of sync.')
                else:
                    method_labels = np.vstack((method_labels, test_labels))
                    method_scores = np.vstack((method_scores, test_scores))
                method_cfs.append(df_cfs)

                logger.info(method['name'], test_scores)
                logger.info('method cfs: {}'.format(method_cfs))
#                if debug:
#                    test_plot_anomalies(test_scores, data, method_name=method['name'])

            # Combine anomaly labels through simple voting
            combined_anomaly_labels = simple_voting(method_labels, method_scores,
                                                    agreement_factor=agreement_factor)
            if norm_flag:
                combined_anomalies = data.df
                combined_anomalies['anomaly_score'] = combined_anomaly_labels / threshold * 1
                combined_anomalies['anomaly_score'] = combined_anomalies['anomaly_score'].clip_upper(10)
                combined_anomalies['anomaly_threshold'] = 1
            else:
                combined_anomalies = data.df.iloc[np.where(combined_anomaly_labels >= 1)[0], :]
                combined_anomalies['anomaly_score'] = [x for x in combined_anomaly_labels if x >= 1]
                combined_anomalies['anomaly_threshold'] = threshold
            # Combine contributing factors through a simple mean
            combined_cfs = simple_mean_of_cfs(combined_anomalies, method_cfs)

            logger.info('combined cfs: {}'.format(combined_cfs))
            try:
                sorted_ca = combined_anomalies.sort_index(ascending=True)
                sorted_cfs = combined_cfs.sort_index(ascending=True)

                ts = sorted_ca.index[-1]
                np_val = combined_anomalies['anomaly_score'].values
                if norm_flag:
                    val_index = np.where(np_val > 1)[0]
                else:
                    val_index = np.where(np_val > threshold)[0]
                selected_cfs = sorted_cfs.iloc[val_index, :]
                mean_cf = selected_cfs.mean(axis=0)
                dict_cf = mean_cf.to_dict()

                val = len(val_index)
                if val > raise_alert_count:
                    flag = 1
                else:
                    flag = 0
            except:
                flag = 0
                ts = data.df.index[-1]
                dict_cf = {}

            logger.info('combined anomaly table: {}'.format(combined_anomaly_labels))
#            if debug:
#                test_plot_anomalies(combined_anomaly_labels, data, method_name='Combined')

            # Format output
            output_datapoints_score = construct_output_score(combined_anomalies, combined_cfs, data.mappings)
            output_datapoints_threshold = construct_output_threshold(combined_anomalies,
                                                                     data.mappings['anomaly_threshold'][0],
                                                                     data.mappings['anomaly_threshold'][1])

            output_datapoints = output_datapoints_score + output_datapoints_threshold
            output_datapoints.append(DataPoint(asset_id=data.mappings['alert_indicator'][0],
                                               channel_key=data.mappings['alert_indicator'][1],
                                               timestamp=ts, value=flag, context=dict_cf))

            analytic_output_payload = AnalyticOutputPayload(outputs=output_datapoints)
            logger.info('AnalyticOutputPayload: {}'.format(analytic_output_payload.to_json()))

            return analytic_output_payload

        except Exception as e:
            logger.exception('Error: {}'.format(e))

            return AnalyticOutputPayload([])

    def train(self, data: DataPayload):

        try:
            # load config_dict and unpack
            allowed_tags = fetch_allowed_tag_list(data)
            trained_model_path = data.parameters.get('trained_model_path',
                                                     ModelPaths.trained_artifacts_pickled_file_path)
            if  trained_model_path is None:
                trained_model_path = ModelPaths.trained_artifacts_pickled_file_path

            # Get methods to train and check validity
            methods = self.get_methods(data)
            if methods is None:
                return AnalyticOutputPayload([])

            # Check whether data is valid
            # TODO - Add data check here.

            # Scale data
            model_df = data.df[allowed_tags]
            data_pipe = get_data_pipe(allowed_tags)
            transformed_data = data_pipe.fit_transform(model_df)
            indices = model_df.index
            data.df = pd.DataFrame(data=transformed_data, index=indices, columns=allowed_tags)
            # Create master model dictionary
            models_dict = dict()
            # Run fit() for each method
            for method in methods:
                args = {x: silent_numerify(method[x]) for x in method if x != 'name'}
                module = [x for x in available_methods if method['name'] in x.__name__][0]
                clf = module(**args)
                clf.fit(np.array(data.df))
                models_dict[method['name']] = {'data-pipe': data_pipe, 'model': clf}

            with open(trained_model_path, 'wb') as f:
                pickle.dump(models_dict, f)

        except Exception as e:
            self.log(e)
            self.log('An unexpected exception occurred and training was not completed.')
            logger.exception('Error: {}'.format(e))
            return False

        return True

    def get_methods(self, data):
        def get_consolidated_method_dict(name, data):
            m = {'name': name}
            for k, v in data.parameters.items():
                if str.startswith(k, name):
                    m[k.strip(name + '-')] = v
            return m

        methods = [k.strip('method-') for k, v in data.parameters.items()
                   if 'method-' in k and str2bool(v)]
        if len(methods) < 1:
            self.log('No methods specified for the selected routine.')
            return None
        if any([x for x in methods if
                x not in [m.__name__ for m in available_methods]]):
            self.log('One or more of the methods specified is not available in this analytic.')
            return None

        methods_consolidated = [get_consolidated_method_dict(x, data) for x in methods]
        return methods_consolidated
