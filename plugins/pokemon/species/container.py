from plugins.pokemon.species.feature import FlagFeature, ChoiceFeature
from plugins.pokemon.species.pokemon import PokemonForm


class PokemonContainer(dict[str, PokemonForm]):
    # gender...TODO
    def __missing__(self, key: str) -> PokemonForm:
        if ' ' not in key:
            raise KeyError(key)

        data = key.split(' ')
        pokemon = self[data[0]]

        # 解析参数 x=y 与 z
        flags = []
        choices = []

        for param in data[1:]:
            if '=' in param:
                key, value = param.split('=')
                choices.append((key, value))
            else:
                flags.append(param)


        aspects = []

        for flag in flags:
            for feature in pokemon.features:
                if feature.isAspect and isinstance(feature, FlagFeature) and flag in feature.keys:
                    aspects.append(flag)


        for choice in choices:
            for feature in pokemon.features:
                if feature.isAspect and isinstance(feature, ChoiceFeature) and choice[0] in feature.keys:
                    aspects.append(feature.aspectFormat.replace("{{choice}}", choice[1]))

        for form in pokemon.forms:
            if all(aspect in form.aspects for aspect in aspects):
                self[key] = form
                return form


        if all(aspect in pokemon.aspects for aspect in aspects):
            self[key] = pokemon
            return pokemon

        raise KeyError(f"can't resolve the key: {key}")


pokemon_container = PokemonContainer()
