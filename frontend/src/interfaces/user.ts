import type { Address } from "./address";

export interface User {
  id?: number;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string | null;
  gender?: string | null;
  addresses: Address[];
}


