import api from './axiosConfig';
import {BiomeSpawn, PokemonForm, SpawnDetail} from '../types/Pokemon.type';

const pokemonCache = new Map<string, PokemonForm>();

// 获取单个宝可梦详情
export const getPokemonByName = async (name: string): Promise<PokemonForm> => {
  if (pokemonCache.has(name)) {
    return pokemonCache.get(name)!!;
  }
  const data: PokemonForm = await api.get(`/pokemon/${name}`);
  pokemonCache.set(name, data);
  return data;
};

export const getSpawnByNameAndIndex = async (name: string, index: number): Promise<SpawnDetail> => {
  return api.get(`/spawn/${name}/${index}`);
};

export const getSpawnBiomeByName = async (name: string): Promise<BiomeSpawn> => {
  return api.get(`/biome/${name}`)
}