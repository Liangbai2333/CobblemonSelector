import api from './axiosConfig';
import { PokemonForm } from '../types/Pokemon.type';

// 获取单个宝可梦详情
export const getPokemonByName = async (name: string): Promise<PokemonForm> => {
  return api.get(`/pokemon/${name}`);
};