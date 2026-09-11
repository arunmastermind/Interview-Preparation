def make_threshold_filter(threshold):
    def is_relevant(score):
        return score >= threshold
    return is_relevant

is_relevant = make_threshold_filter(0.8)
print(is_relevant(0.91)) #True
print(is_relevant(0.65)) #False