## Housing Allowance Simulator

For more information about the housing allowance please check this [document at Finlex](http://www.finlex.fi/fi/laki/alkup/2016/20161533?search%5Btype%5D=pika&search%5Bpika%5D=asumistuki).

### Motivation

Both upper secondary and higher education students will be transferred under the general housing allowance on 1 August 2017. This simulation aims to clarify the immediate effects on students living in rented apartments.

### Installation

For running the program you need to have Python3 interpreter installed. Additionally you need following dependencies.

* NumPy
* Matplotlib

Installation in Windows envirnoment easily with `pip install numpy matplotlib`

### Running the simulation

Run `python main.py` with a set of optional argumeents:

* City
* Number of adults in household
* Number of children in household
* Total income of houshold  
* The range of rents included in simulation
* Fix the inclusion of the rent (heating, water, electricity)

For example `python main.py -a 2 -income 800 -min 200 -max 500 --city Espoo` produces graph about the amount of housing allowance in the rent range of 200 to 500 for two adults living in Espoo with a total income of 800e.

Run `python main.py --help` for more details about running the simulation

### Examples

Examples of the output of the simulation. Blue line represents the paid housing allowance and green line the difference between the rent and the allowance.

![Figure 1](https://github.com/nnevalainen/general-housing-allowance-simulation/blob/master/Figures/figure_1.png)
**Example 1, Single in Espoo**
A student living alone in Espoo with no income besides the study grant. Maximum housing allowance of 394e is paid for housing costs of 514 onwards (including electricity).

![Figure 2](https://github.com/nnevalainen/general-housing-allowance-simulation/blob/master/Figures/figure_2.png)
**Example 2, Single in Turku**
The same situation as before but this time student is living in Turku. The maximum housing allowance of 312e is paid for housing costs of 412 onwards (including electricity).

### Implementation

Program is written in Python3. It uses NumPy and Matplotlib extra packages for visualisation. Data is stored in realtional database and sqlite is used as a SQL database engine.

asumislisa.db contains the constants needed for the simulation as prescribed by Finnish Parliement.

Classes:
* Calculator: handles the calculation
* DbHandler: handles database connetction and sql queries.
