from plugins.pokemon.species.feature import FlagFeature, ChoiceFeature
from plugins.pokemon.species.pokemon import PokemonForm


class PokemonContainer(dict[str, PokemonForm]):

    def get(self, __key, __default=None):
        value = super().get(__key)
        if value:
            return value
        try:
            return self.__missing__(__key)
        except KeyError:
            return __default


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
                if isinstance(feature, ChoiceFeature) and feature.isAspect and choice[0] in feature.keys:
                    aspects.append(feature.aspectFormat.replace("{{choice}}", choice[1]))


        def try_aspects():
            for form in pokemon.forms:
                if all(aspect in aspects for aspect in form.aspects):
                    self[key] = form
                    return form

            return None

        poke = try_aspects()
        if poke:
            return poke
        aspects = data[1:]
        poke = try_aspects()
        if poke:
            return poke


        # Else default
        return pokemon


pokemon_container = PokemonContainer()
