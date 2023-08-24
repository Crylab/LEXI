# !/usr/bin/python
import yaml
import random
from random import randint
from deep_translator import GoogleTranslator
if __name__ == '__main__':
    with open('data.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        verbs = data["verbs"]
        # print(verbs)
        pronouns_list = ["Io", "Tu", "Lei", "Lui", "Noi", "Voi", "Loro"]
        pronouns_reflex = {"Io": "mi", "Tu": "ti", "Lei": "si", "Lui": "si", "Noi": "ci", "Voi": "vi", "Loro": "si"}
        past = {"avere": {"Io": "ho", "Tu": "hai", "Lei": "ha", "Lui": "ha", "Noi": "abbiamo", "Voi": "avete", "Loro": "hanno"},
                "essere": {"Io": "sono", "Tu": "sei", "Lei": "e", "Lui": "e", "Noi": "siamo", "Voi": "siete", "Loro": "sono"}}
        future = {
            "are": {"Io": "ero", "Tu": "erai", "Lei": "era", "Lui": "era", "Noi": "eremo", "Voi": "erete", "Loro": "eranno"},
            "ere": {"Io": "ero", "Tu": "erai", "Lei": "era", "Lui": "era", "Noi": "eremo", "Voi": "erete",
                    "Loro": "eranno"},
            "ire": {"Io": "iro", "Tu": "irai", "Lei": "ira", "Lui": "ira", "Noi": "iremo", "Voi": "irete",
                    "Loro": "iranno"}
        }
        pronouns = {
                    "care": {"Io": "o", "Tu": "hi", "Lei": "a", "Lui": "a", "Noi": "hiamo", "Voi": "ate", "Loro": "ano"},
                    "gare": {"Io": "o", "Tu": "hi", "Lei": "a", "Lui": "a", "Noi": "hiamo", "Voi": "ate",
                             "Loro": "ano"},
                    "iare": {"Io": "o", "Tu": "", "Lei": "a", "Lui": "a", "Noi": "amo", "Voi": "ate", "Loro": "ano"},
                    "are": {"Io": "o", "Tu": "i", "Lei": "a", "Lui": "a", "Noi": "iamo", "Voi": "ate", "Loro": "ano"},
                    "ere": {"Io": "o", "Tu": "i", "Lei": "e", "Lui": "e", "Noi": "iamo", "Voi": "ete", "Loro": "ono"},
                    "ire": {"Io": "o", "Tu": "i", "Lei": "e", "Lui": "e", "Noi": "iamo", "Voi": "ite", "Loro": "ono"},
                    "_ire": {"Io": "isco", "Tu": "isci", "Lei": "isce", "Lui": "isce", "Noi": "iamo", "Voi": "ite", "Loro": "iscono"}}
        past_pronouns = {
                    "are": "ato",
                    "ere": "uto",
                    "ire": "ito"
        }
        data_list = list(verbs)
        while True:
            each = random.choice(data_list)
            attr = []
            if verbs[each] is not None and "attribute" in verbs[each]:
                attr = verbs[each]["attribute"]
            time = randint(0, 2)
            index = randint(0, len(pronouns_list) - 1)
            key = pronouns_list[index]
            reflex = False
            word = each
            if each[-3:] == "rsi":
                reflex = True
                word = each[:-2] + "e"
            if time == 1:  # present
                if verbs[each] is None or "present" not in verbs[each]:
                    ending = word[-4:]
                    if ending not in pronouns:
                        ending = word[-3:]
                    time = randint(0, 1)
                    if "isc" in attr:
                        ending = "_ire"
                    value = pronouns[ending][key]
                    string = word[:-3] + value
                if verbs[each] is not None and "present" in verbs[each]:
                    value = verbs[each]["present"][index]
                    string = value
            elif time == 0:
                if reflex:
                    ending = word[-3:]
                    value = past_pronouns[ending]
                    service = past["essere"][key]
                    string = service + " " + word[:-3] + value
                elif "past_essere" in attr:
                    if verbs[each] is not None and "past_form" in verbs[each]:
                        past_form = verbs[each]["past_form"]
                        service = past["essere"][key]
                        string = service + " " + past_form
                    if verbs[each] is None or "past_form" not in verbs[each]:
                        ending = word[-3:]
                        value = past_pronouns[ending]
                        service = past["essere"][key]
                        string = service + " " + word[:-3] + value
                elif verbs[each] is not None and "past_form" in verbs[each]:
                    past_form = verbs[each]["past_form"]
                    service = past["avere"][key]
                    string = service + " " + past_form
                else:
                    ending = word[-3:]
                    value = past_pronouns[ending]
                    service = past["avere"][key]
                    string = service + " " + word[:-3] + value
                if "past_multiple" in attr:
                    if index > 3:
                        string = string[:-1] + "i"
            elif time == 2:
                if verbs[each] is not None and "future" in verbs[each]:
                    value = verbs[each]["future"][index]
                    string = value
                if verbs[each] is None or "future" not in verbs[each]:
                    ending = word[-3:]
                    value = future[ending][key]
                    string = word[:-3] + value
            if reflex:
                string = key + " " + pronouns_reflex[key] + " " + string
            else:
                string = key + " " + string
            print(string)
            translated = GoogleTranslator(source='it', target='ru').translate(string)
            print(translated)
            break


