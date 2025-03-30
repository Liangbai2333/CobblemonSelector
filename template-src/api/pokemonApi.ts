import api from './axiosConfig';
import {BiomeSpawn, PokemonForm, SpawnDetail} from '../types/Pokemon.type';

// 获取单个宝可梦详情
export const getPokemonByName = async (name: string): Promise<PokemonForm> => {
  return api.get(`/pokemon/${name}`);
};

export const getSpawnByNameAndIndex = async (name: string, index: number): Promise<SpawnDetail> => {
  return api.get(`/spawn/${name}/${index}`);
};

export const getSpawnBiomeByName = async (name: string): Promise<BiomeSpawn> => {
  return api.get(`/biome/${name}`)
}