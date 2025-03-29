// Pokemon.type.ts

// 基础接口
import {I18n, I18nFull} from "./I18n.type.ts";

export interface Stats {
  hp: number;
  attack: number;
  defence: number;
  special_attack: number;
  special_defence: number;
  speed: number;
}

export interface Ability extends I18nFull {
  prefix: string;
  name: string;
}

export interface EggGroup extends I18n {
  name: string;
}

export interface Move extends I18nFull {
  condition: number | string;
  name: string;
}

// Evolution 相关接口
export interface EvolutionRequirement extends I18n {
  variant: string;
}

// EvolutionRequirement 的子类型
export interface AnyRequirement extends EvolutionRequirement {
  variant: "any";
  possibilities: EvolutionRequirement[];
}

export interface AABB {
  minX: number;
  minY: number;
  minZ: number;
  maxX: number;
  maxY: number;
  maxZ: number;
}

export interface Area extends EvolutionRequirement {
  variant: "area";
  box: AABB;
}

export enum AttackDefenceRatioEnum {
  ATTACK_HIGHER = "attack_higher",
  DEFENCE_HIGHER = "defence_higher",
  EQUAL = "equal"
}

export interface AttackDefenceRatio extends EvolutionRequirement {
  variant: "attack_defence_ratio";
  ratio: AttackDefenceRatioEnum;
}

export interface BiomeRequirement extends EvolutionRequirement {
  variant: "biome";
  biomeCondition?: string;
  biomeAnticondition?: string;
}

export interface BlocksTraveledRequirement extends EvolutionRequirement {
  variant: "blocks_traveled";
  amount: number;
}

export interface DamageTaken extends EvolutionRequirement {
  variant: "damage_taken";
  amount: number;
}

export interface Defeat extends EvolutionRequirement {
  variant: "defeat";
  target: string;
  amount: number;
}

export interface Friendship extends EvolutionRequirement {
  variant: "friendship";
  amount: number;
}

export interface HeldItem extends EvolutionRequirement {
  variant: "held_item";
  itemCondition: string;
}

export interface Level extends EvolutionRequirement {
  variant: "level";
  minLevel: number;
  maxLevel: number;
}

export interface MoonPhase extends EvolutionRequirement {
  variant: "moon_phase";
  moonPhase: string;
}

export interface MoveSet extends EvolutionRequirement {
  variant: "has_move";
  move: string;
}

export interface MoveType extends EvolutionRequirement {
  variant: "has_move_type";
  type: string;
}

export interface PartyMember extends EvolutionRequirement {
  variant: "party_member";
  target: string;
  contains: boolean;
}

export interface PlayerHasAdvancement extends EvolutionRequirement {
  variant: "advancement";
  requiredAdvancement: string;
}

export interface PokemonProperties extends EvolutionRequirement {
  variant: "properties";
  target: string;
}

export interface PropertyRange extends EvolutionRequirement {
  variant: "property_range";
  range: [number, number];
  feature: Feature;
}

export interface Recoil extends EvolutionRequirement {
  variant: "recoil";
  amount: number;
}

export interface StatCompare extends EvolutionRequirement {
  variant: "stat_compare";
  highStat: string;
  lowStat: string;
}

export interface StatEqual extends EvolutionRequirement {
  variant: "stat_equal";
  statOne: string;
  statTwo: string;
}

export interface Structure extends EvolutionRequirement {
  variant: "structure";
  structureCondition?: string;
  structureAnticondition?: string;
}

export type TimeRangeValue =
  | "any"
  | "day"
  | "night"
  | "noon"
  | "midnight"
  | "dawn"
  | "dusk"
  | "twilight"
  | "morning"
  | "afternoon"
  | "predawn"
  | "evening";

export interface TimeRange extends EvolutionRequirement {
  variant: "time_range";
  range: TimeRangeValue;
}

export interface UseMove extends EvolutionRequirement {
  variant: "use_move";
  move: string;
  amount: number;
}

export interface WeatherRequirement extends EvolutionRequirement {
  variant: "weather";
  isRaining?: boolean;
  isThundering?: boolean;
}

export interface World extends EvolutionRequirement {
  variant: "world";
  identifier: string;
}

export interface BattleCriticalHits extends EvolutionRequirement {
  variant: "battle_critical_hits";
  amount: number;
}

export interface Evolution extends I18n {
  id: string;
  variant: string;
  result: string;
  optional: boolean;
  consumeHeldItem: boolean;
  learnableMoves: Move[];
  requirements: EvolutionRequirement[];
  requiredContext?: string;
}

// Biome 相关接口
export interface BiomeValueRef {
  id: string;
  required: boolean;
}

export interface Biome extends I18n {
  translation_name?: string;
  replace: boolean;
  values: (string | BiomeValueRef)[];
  details?: any[];
}

// SpawnDetail 相关接口
export type SpawnContext = "grounded" | "seafloor" | "lavafloor" | "submerged" | "surface" | "fishing";

export interface Preset extends I18n {
  name: string;
}

export type SpawnBucketType = "common" | "uncommon" | "rare" | "ultra-rare"

export interface SpawnBucket extends I18n {
  name: SpawnBucketType;
  weight: number;
}

export interface SpawnCondition {
  biomes: Biome[];
  liked_biomes: string[];
  moonPhase?: string | number;
  canSeeSky?: boolean;
  minX?: number;
  minY?: number;
  minZ?: number;
  maxX?: number;
  maxY?: number;
  maxZ?: number;
  minLight?: number;
  maxLight?: number;
  minSkyLight?: number;
  maxSkyLight?: number;
  isRaining?: boolean;
  isThundering?: boolean;
  timeRange?: string;
  isSlimeChunk?: boolean;
}

export interface WeightMultiplier {
  condition?: SpawnCondition;
  anticondition?: SpawnCondition;
  multiplier: number;
}

export interface SpawnDetail {
  enabled: boolean;
  pokemon: string;
  type: "pokemon" | "npc";
  presets: Preset[];
  context: SpawnContext;
  bucket: SpawnBucket;
  level: string;
  weight: number;
  condition?: SpawnCondition;
  anticondition?: SpawnCondition;
  weightMultiplier?: WeightMultiplier;
  percentage?: number;
  labels: string[];
}

// Feature 基础接口
export interface Feature {
  type: string;
  visible: boolean;
  needsKey: boolean;
  keys: string[];
  isAspect: boolean;
}

// IntFeature 接口
export interface DisplayData {
  name: string;
}

export interface IntFeature extends Feature {
  type: "integer";
  default: number;
  min: number;
  max: number;
  display?: DisplayData;
  isAspect: boolean;
}

// ChoiceFeature 接口
export interface ChoiceFeature extends Feature {
  type: "choice";
  default?: string;
  isAspect: boolean;
  aspectFormat: string;
}

// FlagFeature 接口
export interface FlagFeature extends Feature {
  type: "flag";
  default?: "random" | boolean;
  isAspect: boolean;
}

export type PokemonType = 'normal' | 'fire' | 'water' | 'grass' | 'electric' | 'ice' |
                  'fighting' | 'poison' | 'ground' | 'flying' | 'psychic' |
                  'bug' | 'rock' | 'ghost' | 'dragon' | 'dark' | 'steel' | 'fairy';

// 主要的PokemonForm接口
export interface PokemonForm extends I18nFull {
  species?: string;
  original_name?: string;
  name: string;
  primaryType: PokemonType;
  secondaryType?: PokemonType;
  maleRatio: number;
  height: number;
  weight: number;
  pokedex?: string[];
  labels?: string[];
  abilities?: Ability[];
  eggGroups?: EggGroup[];
  aspects: string[];
  baseStats?: Stats;
  baseExperienceYield?: number;
  evYield?: Stats;
  moves: Move[];
  preEvolution?: string;
  evolutions: Evolution[];
  battleOnly?: boolean;
  experienceGroup?: string;
  catchRate?: number;
  eggCycles?: number;
  baseFriendship?: number;
  biomes?: Biome[];
  spawn_details?: SpawnDetail[];

  // 额外的序列化字段
  search_name: string;
  image_url: string;
  pokedex_number: string;
}

// Pokemon 接口，继承自 PokemonForm
export interface Pokemon extends PokemonForm {
  implemented: boolean;
  nationalPokedexNumber: number;
  features: Feature[];
  forms: PokemonForm[];
}