# Note: We can use Pandas DataFrame for enhanced reporting
import json
import multiprocessing
from config import logger

# Created bmi_category dict to get category in O(1) time
bmi_category = {
    0: {'category': 'Underweight', 'health_risk': 'Malnutrition risk'},
    18.5: {'category': 'Normal weight', 'health_risk': 'Low risk'},
    25: {'category': 'Overweight', 'health_risk': 'Enhanced risk'},
    30: {'category': 'Moderately obese', 'health_risk': 'Medium risk'},
    35: {'category': 'Severely obese', 'health_risk': 'High risk'},
    40: {'category': 'Very severely obese', 'health_risk': 'Very high risk'},
}
# Created bmi_results list as final list after all task completion
bmi_results = []
# Created category_count dict to identify specific people count of BMI Category
category_count = {}
for key in bmi_category.keys():
    category_count[key] = 0

def bmi_calculation():
    logger.info('BMI Calculation started.')
    categories = list(bmi_category.keys())
    with open('data/weight_height_data.json', 'r') as data:
        wg_ht_data = json.load(data)
        logger.info('Successfully read json file.')

    # Parallel processing based on cpu count as BMI calculation is not dependent on each other.
    logger.info('Started BMI calculation in parallel mode.')
    cpu_cnt = multiprocessing.cpu_count()
    pool = multiprocessing.Pool()
    result = [pool.apply(_calculate, args = (categories, category_count, wg_ht_data[i:i + cpu_cnt])) for i in range(0, len(wg_ht_data), cpu_cnt)]
    logger.info('BMI calculation completed with {} cpu cores.'.format(cpu_cnt))
    for r in result:
        bmi_results.extend(r[0])
        for key in category_count.keys():
            category_count[key] += r[1][key]

    bmi_category_count = {
        'underweight_people': category_count[0],
        'normal_weight_people': category_count[18.5],
        'overweight_people': category_count[25],
        'moderately_obese_people': category_count[30],
        'severely_obese_people': category_count[35],
        'very_severely_obese_people': category_count[40]
    }
    logger.info('BMI Calculation completed.')

    print('Calculated BMI with Category and Health Risk: {}'.format(bmi_results))
    print('************************************************')
    print('Underweight people count: {}'.format(category_count[0]))
    print('Normal weight people count: {}'.format(category_count[18.5]))
    print('Overweight people count: {}'.format(category_count[25]))
    print('Moderately obese people count: {}'.format(category_count[30]))
    print('Severely obese people count: {}'.format(category_count[35]))
    print('Very severely obese people count: {}'.format(category_count[40]))

    return {'bmi_with_category': bmi_results, 'category_wise_count': bmi_category_count}

def _calculate(categories, category_count, lst):
    logger.info('Started BMI calculation for list:', lst)
    for item in lst:
        # Calculating BMI
        item['bmi'] = round(item['WeightKg']/(item['HeightCm']/100), 1)
        # Searching for BMI Category based on calculated BMI
        key = _searchCategory(categories, item['bmi'], 0, len(categories)-1)
        item['category'] = bmi_category[key]['category']
        item['health_risk'] = bmi_category[key]['health_risk']
        category_count[key] += 1
    return lst, category_count

# used binary search to minimize time to search as keys are already sorted
def _searchCategory(categories, bmi, l, r):
    logger.info('Started to search category based on BMI:', bmi)
    if r >= l:
        mid = l + (r - l) // 2
        if categories[mid] <= bmi and (mid == len(categories)-1 or categories[mid+1] > bmi):
            return categories[mid]
        elif categories[mid] > bmi:
            return _searchCategory(categories, bmi, l, mid-1)
        else:
            return _searchCategory(categories, bmi, mid+1, r)
