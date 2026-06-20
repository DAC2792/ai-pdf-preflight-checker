import yaml

#Open and return "Rules" for pass/fail from the preflight_rules.yaml in config
def load_rules(filepath):
    with open(filepath) as file:
        rules = yaml.safe_load(file)
    return rules

#Check resolution of the image and produce a dpi pass/fail response against the image page number
def check_resolution(dpi, page_number, rules):
    min_dpi = rules["resolution"]["min_dpi"]
    if dpi >= min_dpi:
        result = "pass"
    else:
        result = "fail"
    return {"check": "resolution", "page": page_number, "dpi": dpi, "result": result}
    
if __name__ == "__main__":
    rules = load_rules("config/preflight_rules.yaml")
    result = check_resolution(50.8, 1, rules)
    print(result)