import random

class Centroid:
    def __init__(self, location):
        self.location = location
        self.closest_users = set()

NUM_FEATURES_PER_USER = 4

# PCA Transformed Data
USER_FEATURE_MAPS = {
    'uid_1' : [-1.345666, 1.34563, 2.45633, -2.34567],
    'uid_2' : [-1.345666, 1.34563, 2.45633, -2.34567],
    'uid_3' : [-1.345666, 1.34563, 2.45633, -2.34567],
    'uid_4' : [-1.345666, 1.34563, 2.45633, -2.34567],
    'uid_5' : [-1.345666, 1.34563, 2.45633, -2.34567]
}


def get_k_means(k):

    # This is to ensure to get the value same for every run
    random.seed(42)

    # Extracting user_id randomly based on cluster (k) value
    initial_centroid_users = random.sample(sorted(list(USER_FEATURE_MAPS.keys())), k)

    # Get the Feature of that user_id being considered as centroid & initiate Centrod object by assigning location of it
    centroids = [Centroid(USER_FEATURE_MAPS[initial_centroid_user]) for initial_centroid_user in initial_centroid_users]

    for _ in range(10): # Total no of iteration to get the ideal cluster

        # Iterate through all the users & their corresponding features
        for users_id, features in USER_FEATURE_MAPS.items():
            closest_centroid_distance = float('inf')
            closest_centroid = None

            # Iterate through all the centroid to find invidual user's closeness towards that cluster's centroid
            for centroid in centroids:
                feature_to_centroid_distance = get_manhattan_distance(features, centroid.location) # Manhattan Distance

                # Update cosest centroid for a particular feature
                if feature_to_centroid_distance < closest_centroid_distance:
                    closest_centroid_distance = feature_to_centroid_distance
                    closest_centroid = centroid
            
            # Update user_id for corresponding cluster 
            closest_centroid.closest_users.add(users_id)

        # Calulate average of all the user feature & to find new centroid
        for centroid in centroids:
            centroid.location = get_centroid_average(centroid) # Centroid Average
            centroid.closest_users.clear() # Clear all the users once centroid is found

    return [centroid.location for centroid in centroids] # Return the final centroid

# Manhattan Distance - Absolute difference between 2 data point(s)
def get_manhattan_distance(features, other_features):
    absolute_differences = []
    for i in range(len(features)):
        absolute_differences.append(abs(features[i] - other_features[i]))

    return sum(absolute_differences)

# Calucale centroid Average
def get_centroid_average(centroid):
    centroid_average = [0] * NUM_FEATURES_PER_USER
    for i in range(NUM_FEATURES_PER_USER):
        for user in centroid.closest_users:
            centroid_average[i] += USER_FEATURE_MAPS[user][i]

    return [centroid_dimension / len(centroid.closest_users) for centroid_dimension in centroid_average]