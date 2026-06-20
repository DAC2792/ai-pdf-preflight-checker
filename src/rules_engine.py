import yaml

#Open and return "Rules" for pass/fail from the preflight_rules.yaml in config
def load_rules(filepath):
    with open(filepath) as file:
        rules = yaml.safe_load(file)
    return rules




if __name__ == "__main__":
    rules = load_rules("config/preflight_rules.yaml")
    print(rules)