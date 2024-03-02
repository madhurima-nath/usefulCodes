from preprocess.json_preprocess import ParseJsonFunction

class CreateGroupDict:
    """
    create dict from preprocessed json data
    """

    @staticmethod
    def create_dict(json_data, group_list, feature_list) -> dict:
        """
        function to create group dictionary where key-value pair
        represents group-list of features with corresponding scores
        """
        group_dict = {}

        for group in range(len(group_list)):
            # initialize empty list for each group
            values = []

            for idx in range(len(feature_list)):
                values.append(
                    ParseJsonFunction.get_score(json_data, group, idx)
                )
            group_dict[group_list[group]] = values
        return group_dict