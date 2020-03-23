import os
import yaml

print("\nThank you for using Tiky's term life insurance coverage calculator!")
print("Please key in your details accurately, or you'll have to restart\n")

def load_cfg(yaml_filepath):
    """
    Load a YAML configuration file.
    Parameters
    ----------
    yaml_filepath : str
    Returns
    -------
    cfg : dict
    """
    # Read YAML experiment definition file
    with open(yaml_filepath, 'r') as stream:
        cfg = yaml.load(stream)
    cfg = make_paths_absolute(os.path.dirname(yaml_filepath), cfg)
    return cfg

def make_paths_absolute(dir_, cfg):
    """
    Make all values for keys ending with `_path` absolute to dir_.
    Parameters
    ----------
    dir_ : str
    cfg : dict
    Returns
    -------
    cfg : dict
    """
    for key in cfg.keys():
        if key.endswith("_path"):
            cfg[key] = os.path.join(dir_, cfg[key])
            cfg[key] = os.path.abspath(cfg[key])
            if not os.path.isfile(cfg[key]):
                logging.error("%s does not exist.", cfg[key])
        if type(cfg[key]) is dict:
            cfg[key] = make_paths_absolute(dir_, cfg[key])
    return cfg


def calculating_life_coverage():
	loaded= load_cfg("config.yaml")

	try:
		age=float(input("Enter your age: "))
	except:
		print("Error: Please enter a number instead..\n")
		return

	try:
		retire_age=float(input("Enter your age that you want to retire...\n(ie. Age when you have enough money for yourself to live rest of your life): "))
	except:
		print("Error: Please enter a number instead..\n")
		return

	try:
		income=float(input("Enter your current monthly income: $"))
	except:
		print("Error: Please enter a number instead..\n")
		return

	try:
		expenses=float(input("Enter your current monthly expenses: $"))
	except:
		print("Error: Please enter a number instead..\n")
		return

	try:
		assets=float(input("Enter the total amount of bank savings and liquid investments you have: $"))
	except:
		print("Error: Please enter a number instead..\n")
		return

	try:
		loans=float(input("Enter the total amount of loans you have: $"))
	except:
		print("Error: Please enter a number instead..\n")
		return

	try:
		dependents=float(input("How many dependents do you have to support?: "))
	except:
		print("Error: Please enter a number instead..\n")
		return


	years_needing_income=retire_age-age
	networth=assets-loans
	required_networth_considering_dependents=loaded['money_needed_by_each_dependent']*dependents #default to $285,000 to raise dependent to adulthood...Source: https://blog.seedly.sg/cost-raise-child-singapore/
	inflation_rate=loaded['inflation'] #default to 2% inflation rate per annum
	

	if years_needing_income<=0:
		inflation_factor=inflation_rate**10 #default to 10 years
	else:
		inflation_factor=inflation_rate**(years_needing_income)


	if years_needing_income <=0 and (networth-required_networth_considering_dependents) >=0:
		print("\nYou can focus on growing your money further at this point using investments instead!\n")
		return 
	elif years_needing_income<=0 and (networth-required_networth_considering_dependents) <0:
		life_coverage=required_networth_considering_dependents*inflation_factor + loans
	else:
	    life_coverage=expenses*12*years_needing_income*inflation_factor + 0.5*required_networth_considering_dependents*(inflation_rate**10)+ loans #0.5 factor for require networth assuming expenses already catered for dependents, so extra money for them


	if (income-expenses<=0):
		critical_illness_coverage=(expenses*12*5)*(inflation_rate**5)+loaded['money_for_alternative_treatment'] #extra $160,000 for alternative treatments if needed
	else:
		critical_illness_coverage=(income*12*5)*(inflation_rate**5)+loaded['money_for_alternative_treatment'] #extra $160,000 for alternative treatments if needed


	early_critical_illness_coverage=0.25*critical_illness_coverage


	print("\nYour total Life Insurance coverage needed is: {}".format(life_coverage))
	print("Your total Critical Illness Insurance coverage needed is: {}".format(critical_illness_coverage))
	print("Your total Early Critical Illness Insurance coverage needed is: {}".format(early_critical_illness_coverage))

calculating_life_coverage()