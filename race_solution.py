"""
This is a stub for the comp16321 midterm.
Do not edit or delete any lines given in this file that are marked with a "(s)".
(you can move them to different lines as long as you do not change the overall structure)

Place your code below the comments marked "#Your code here".

Each method is documented to explain what work is to be placed within it.

NOTE: You can create as many more methods as you need. However, you need to add 
self as a parameter of the new method and to call it with the prefix self.name 

EXAMPLE:

def class_table_result(self, boat_type, race_results):#(s)
    strings_value = "0601-0501-0702-0803-0904-0405-0306-0207-1008-0609-0110"
    single_boat = self.remove_highest_value(strings_value)
    return(single_boat)

def remove_highest_value(self, strings_value):
    strings_value.pop(10)
    return strings_value

"""

class Races:#(s)

    def read_results(self):#(s)
        with open('input.txt', 'r') as file:
            results_string = file.readlines()
        
        results_string = [line.strip() for line in results_string]
        return results_string
        """
        Read in the text file and save the races_results into a python list

        :return: A list of strings denoting each race_result
        """
        # Your code here

        pass#(s)

    def race_result(self, boat_type, race_number, results_string):
        count = 0
        for race in results_string:
            current_boat_type = int(race[:2])  
            if current_boat_type == boat_type:
                count += 2
                if count == race_number:
                    start_index = 5 if race[4] == '-' else 4
                    return race[start_index:].strip() 

        return ""

        """
        Query results_string which is read form the input.txt and  get the  result
        for the given params
        
        :param: boat_type: An integer denoting which type of boat 
        :param: race_number: An integer denoting which race
        :return: A string with the race result for the given boat_type and race_number
        """
        # Your code here

        pass#(s)

    def class_table_result(self, boat_type, results_string):#(s)
        country_points = {str(i).zfill(2): 0 for i in range(1, 11)}  
        last_race_order = []

        for race in results_string:
            current_boat_type, race_type = race[:2], race[2:4]
            if current_boat_type == str(boat_type).zfill(2):
                race_results = race[5:].split('-')  

                adjusted_results = []
                disqualified = []
                for result in race_results:
                    if result.endswith('xx'):
                        disqualified_country = result[:2]
                        disqualified.append(disqualified_country)
                        points = 11 if race_type == '01' else 22  
                        country_points[disqualified_country] += points
                    else:
                        adjusted_results.append(result)

                for position, result in enumerate(adjusted_results, start=1):
                    country = result[:2]
                    points = position * (2 if race_type == '02' else 1)  
                    country_points[country] += points

                last_race_order = [result[:2] for result in race_results]

        sorted_countries = sorted(country_points.items(), key=lambda x: (x[1], last_race_order.index(x[0]) if x[0] in last_race_order else float('inf')))

        formatted_results = []
        for position, (country, points) in enumerate(sorted_countries, start=1):
            formatted_results.append(f"{country}-{str(position).zfill(2)}-{points}")

        return ", ".join(formatted_results)


        """
        Output the results for a given boat_type

        :param: boat_type: An integer denoting which type of boat 
        :return: A string in the specified format as shown in the pdf
        """

        # Your code here

        pass#(s)

    def class_table_discard_result(self, boat_type, results_string):#(s)
        singles = []
        doubles = []

        races = [x for x in results_string if x.startswith(str(boat_type).zfill(2))] # get only the races that we want

        for race in races:
            r = {k: v for k, v in [[j[:2], int(j[2:]) if not j[2:].endswith("xx") else 11] for j in race[5:].split('-')]} # get the scores of each race formatted properly
            if int(race[2:4]) == 1: # if double or single pointer race, etc.
                singles.append(r)
            else:
                doubles.append(r)

        
        if len(singles) > 2:
            removal = {k: max([x[k] for x in singles]) for k in singles[0].keys()} # take the minimum value for each country
            total_single = {k: sum([x[k] for x in singles]) - removal[k] for k in singles[0].keys()} # and add scores while subtracting the minimum value
        else:
            total_single = {k: sum([x[k] for x in singles]) for k in singles[0].keys()} # otherwise just add the scores
        
        if len(doubles) > 2:
            removal = {k: max([x[k] for x in doubles]) for k in doubles[0].keys()}
            total_double = {k: sum([x[k] for x in doubles]) - removal[k] for k in doubles[0].keys()}
        else:
            total_double = {k: sum([x[k] for x in doubles]) for k in doubles[0].keys()}

        total = {k: total_single[k] + total_double[k]*2 for k in total_single.keys()} # add the single and double scores together

        sorted_countries = sorted(total.items(), key=lambda x: (x[1], x[0]))
        output = []
        for i in range(len(sorted_countries)):
            output.append(f"{sorted_countries[i][0]}-{str(i+1).zfill(2)}-{sorted_countries[i][1]}")
        return ", ".join(output)
        """
        Output the class table discard string

        :param: boat_type: An integer denoting which type of boat 
        :return: A string in the specified format as shown in the pdf
        """
        # Your code here

        pass#(s)

    def medal_table_result(self, results_string):#(s)
        medals = {str(i).zfill(2): {'gold': 0, 'silver': 0, 'bronze': 0} for i in range(1, 11)}
        
        for boat_type in range(1, 11):  
            class_results = self.class_table_discard_result(boat_type, results_string)

            
            for position, result in enumerate(class_results.split(', ')):
                if position > 2:
                    break  
                country = result.split('-')[0]
                if position == 0: 
                    medals[country]['gold'] += 1
                elif position == 1: 
                    medals[country]['silver'] += 1
                elif position == 2: 
                    medals[country]['bronze'] += 1

        for country in medals:
            medals[country]['total'] = (medals[country]['gold'] * 3) + (medals[country]['silver'] * 2) + medals[country]['bronze']

        sorted_countries = sorted(medals.items(), key=lambda x: (-x[1]['total'], -x[1]['gold'], -x[1]['silver'], -x[1]['bronze'], x[0]))

        output = [f"{country}-{medal_counts['gold']}-{medal_counts['silver']}-{medal_counts['bronze']}-{medal_counts['total']}" for country, medal_counts in sorted_countries]
        return ', '.join(output)

        """
        Output the class table discard string

        :param: boat_type: An integer denoting which type of boat 
        :return: A string in the specified format as shown in the pdf 
        """

        # Your code here

        pass#(s)


if __name__ == '__main__':#(s)
    
    pass#(s)
