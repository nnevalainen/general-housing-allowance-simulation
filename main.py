
from db import DbHandler
import numpy as np
import matplotlib.pyplot as plt

import argparse

class Calculator:

    """
    Get the total benefit
    @param: INT adults - number of adults
    @param: INT children - number of children
    @param: FLOAT income
    @param: STRING city
    """

    DB = "asumislisa.db"

    def __init__(self, adults, chilren, income, city, discard_electricity):

        self.api = DbHandler(Calculator.DB)
        self.adults = adults
        self.children = chilren
        self.income = income
        self.city_group = self.get_city_group(city)
        self.discard_electricity

    def get_city_group(self, city):
        city = city.strip().upper()
        return self.api.find_city(city)

    def discard_electricity(self, rent):
        """
        The constant is estimated from the data of an existing
        KELA calculator. No official method for discarding the electricity
        was publicly available.
        """
        return rent - 22.2

    def get_excess(self):
        """
        Calculates the excess. Constants are determined by KELA

        """
        return max(0, 0.42*(self.income - (597 + 99*self.adults + 221*self.children)))

    def get_acceptable_expenses(self, rent):
        """
        Get the amount of expenses counted as acceptable
        TODO - count more parameters:
            heating included/not included
            water included/not included
        """
        acceptable = self.discard_electricity(rent) if self.discard_electricity else rent
        return acceptable

    def get_total_benefit(self, rent):

        household = self.adults + self.children
        max_benefit = self.api.get_benefit(household, self.city_group)
        acceptable_expenses = self.get_acceptable_expenses(rent)
        acceptable_expenses = min(max_benefit, acceptable_expenses)
        excess = self.get_excess()
        return max(0, 0.8*(acceptable_expenses - excess))


def plot(rent, benefit, to_be_paid, city, adults, children, income):

    fig = plt.figure()

    """ Set y axes"""
    _min = 0
    _max = np.amax(rent)
    axes = plt.gca()
    axes.set_ylim([0 , _max])

    plt.plot(rent, benefit, label="asumislisä")
    plt.plot(rent, to_be_paid, label="itse kustannettavaa")
    plt.legend(shadow=True, fancybox=True)
    plt.grid()
    plt.title("{:}\nAdults={:} Children={:} Income={:}e".format(city, adults, children, income))
    plt.xlabel("Rent")
    plt.show()

def plot_benefit(city, income, adults, children, rent_from, rent_to, discard_electricity):

    calculator = Calculator(adults, children, income, city, discard_electricity)
    f = np.vectorize(calculator.get_total_benefit)

    rent = np.arange(rent_from, rent_to, 1)
    benefit = f(rent)
    to_be_paid = rent - benefit

    plot(rent, benefit, to_be_paid, city, adults, children, income)

def main():

    """ Defaults """
    CITY ="Turku"
    ADULTS = 1
    CHILDREN = 0
    INCOME = 600
    RENT_FROM = 200
    RENT_TO = 800

    parser = argparse.ArgumentParser(description='Calculate the amount of benefit for given rent, city, size of houshold and amount of income')
    parser.add_argument("-i", "--income", type=int, default=INCOME, help="The amount of total household income (default: {})".format(INCOME))
    parser.add_argument("-a", '--adults', type=int, default=ADULTS, help="The number of adults living in household (default: {})".format(ADULTS))
    parser.add_argument("-c", '--children', type=int, default=CHILDREN, help="The number of children (under 18) living in household (default: {})".format(CHILDREN))
    parser.add_argument("-min", default=RENT_FROM, type=int, help="Minimum rent (default {})".format(RENT_FROM))
    parser.add_argument("-max", default=RENT_TO, type=int, help="Maximum rent (default: {})".format(RENT_TO))
    parser.add_argument('--city', default=CITY, help="Specify city (default {:})".format(CITY))
    parser.add_argument('-e', '--electricity', help="Make electricity not included")

    args = parser.parse_args()
    electricity_included = False if args.electricity else True

    plot_benefit(args.city, args.income, args.adults, args.children, args.min, args.max, electricity_included)

main()
