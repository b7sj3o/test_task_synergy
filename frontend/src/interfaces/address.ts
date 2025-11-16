import type { Timezone } from "./timezone";

export interface Address {
  id?: number;
  street: string;
  city: string;
  state?: string | null;
  country: string;
  postcode?: string | null;
  timezone?: Timezone | null;
}


