__author__ = 'Akshay'

"""
File contains code to Mine reviews and stars from a state reviews.

This is just an additional POC that we had done on YELP for visualising number of 5 star reviews per state on a map.
For each business per state, 5 reviews are taken and the count of the review is kept in the dictionary for each state.

Use the resulting json to plot it onto the map.
For the actual map visualisation, please refer State Review Nightlife POC.

Since only 5 business reviews were taken per state, this still needs work.
"""
##############################################

from __future__ import division
import sys
reload(sys)
import json
import datetime

sys.setdefaultencoding('utf8')

state_5_star_dict = {}
state_4_star_dict = {}
state_3_star_dict = {}
state_2_star_dict = {}
state_1_star_dict = {}
state_business = {}


def create_set_for_business_with_cat(category):
    business_count = 0

    with open('Data\yelp_academic_dataset_business.json') as fp:
        for line in fp.readlines():
            temp = json.loads(line, encoding='utf-8')
            categories = str(temp["categories"])
            state = str(temp["state"])

            if state == "ON" or state == "ELN" or state == "EDH" or state == "MLN" or state == "NTH" or state == "FIF":
                continue

            if state not in state_business:
                state_business[state] = 0

            if len(state_business.keys()) == 50:
                break

            if category in categories:
                print state
                business_id = str(temp["business_id"])
                city = str(temp["city"])
                name = str(temp["name"])
                create_yelp_set(business_id, state, city, name)

    print "set prepared."


def create_yelp_set(business_id, state, city, name):
    file_write = open('Data\state_stars_date_business.txt', mode='a')

    if state_business[state] == 5:
        print state, " is already completed."
        return

    with open('Data\yelp_academic_dataset_review.json') as fp:
        for line in fp.readlines():
            temp = json.loads(line, encoding='utf-8')

            if str(temp["business_id"]) == business_id:
                state_business[state] += 1

                star = str(temp["stars"])
                date = str(temp["date"])
                date_tm = datetime.datetime.strptime(date, "%Y-%m-%d").date()

                file_write.write(business_id)
                file_write.write('\t')

                file_write.write(state)
                file_write.write('\t')

                file_write.write(star)
                file_write.write('\t')

                file_write.write(city)
                file_write.write('\t')

                file_write.write(name)
                file_write.write('\t')

                file_write.write(str(date_tm))
                file_write.write('\n')

                if state_business[state] == 5:
                    break

        for key, value in state_5_star_dict.iteritems():
            print key, value

    file_write.close()
    print "Done."


def state_review_trends():
    count = 0

    with open('Data\state_stars_date_business.txt') as fp:
        for line in fp.readlines():
            count += 1
            tup = (line.split("\t")[0], line.split("\t")[1], line.split("\t")[2], line.split("\t")[3],
                   line.split("\t")[4], line.split("\t")[5])
            state = tup[1]
            star_rating = int(tup[2])

            if int(star_rating) != 5:
                continue

            if state not in state_5_star_dict:
                state_5_star_dict[state] = 0

            if state not in state_4_star_dict:
                state_4_star_dict[state] = 0

            if state not in state_3_star_dict:
                state_3_star_dict[state] = 0

            if state not in state_2_star_dict:
                state_2_star_dict[state] = 0

            if state not in state_1_star_dict:
                state_1_star_dict[state] = 0

            if star_rating == 5:
                state_5_star_dict[state] += 1

            if star_rating == 4:
                state_4_star_dict[state] += 1

            if star_rating == 3:
                state_3_star_dict[state] += 1

            if star_rating == 2:
                state_2_star_dict[state] += 1

            if star_rating == 1:
                state_1_star_dict[state] += 1

    response = []
    print "Number of 5 star reviews per state."
    for key, value in state_5_star_dict.iteritems():
        response.append({'id': key, 'value': value})
        print key, value

    json_data = json.dumps(response)


    print json_data
    print "Done."
    print count


def main():
   # Uncomment the line to run mining data.
   # create_set_for_business_with_cat("Nightlife")
    state_review_trends()


if __name__ == "__main__":
    print "Execute Script!!"
    main()
