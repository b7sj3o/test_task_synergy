import { User } from "../interfaces";

export const validateUser = (user: User): string | null => {
    if (!user.first_name?.trim()) {
      return "Ім'я є обов'язковим полем";
    }
  
    if (!user.last_name?.trim()) {
      return "Прізвище є обов'язковим полем";
    }
  
    if (!user.email?.trim()) {
      return "Email є обов'язковим полем";
    }
  
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(user.email.trim())) {
      return "Некоректний формат email";
    }
  
    const [address] = user.addresses ?? [];
  
    if (!address) {
      return "Потрібна щонайменше одна адреса";
    }
  
    if (!address.street?.trim()) {
      return "Поле \"Вулиця\" є обов'язковим";
    }
  
    if (!address.city?.trim()) {
      return "Поле \"Місто\" є обов'язковим";
    }
  
    if (!address.country?.trim()) {
      return "Поле \"Країна\" є обов'язковим";
    }
  
    return null;
  };