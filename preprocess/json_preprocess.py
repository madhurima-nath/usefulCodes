class ParseJsonFunction:
    """
    Helper class to parse JSON file
    """

    @staticmethod
    def get_score(json_data, group_index, feature_index) -> tuple:
        """
        function to get probability score for 
        listed features in the json file
        """

        rowLabels = json_data["result"]["rowLabels"][feature_index]
        prob_score = json_data["result"]["scores"][feature_index][group_index]["prob_score"]
        mean_score = json_data["result"]["scores"][feature_index][
                        group_index]["mean_score"]
        
        out_tuple = (rowLabels, prob_score, mean_score)

        return out_tuple