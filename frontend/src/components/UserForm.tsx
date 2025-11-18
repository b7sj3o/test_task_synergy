import { useEffect, useState } from "react";
import type { User } from "../interfaces";

type Props = {
  initial: User;
  onSubmit: (u: User) => Promise<void> | void;
  submitText?: string;
};

export default function UserForm({
  initial,
  onSubmit,
  submitText = "Зберегти",
}: Props) {
  const [user, setUser] = useState<User>(initial);

  useEffect(() => {
    setUser(initial);
  }, [initial]);

  const updateField = <K extends keyof User>(key: K, value: User[K]) => {
    setUser((prev) => ({ ...prev, [key]: value }));
  };

  const addresses = user.addresses ?? [];
  const mainAddress = addresses[0] ?? {
    street: "",
    city: "",
    country: "",
  };

  const mainTimezone = mainAddress.timezone ?? {
    offset: "",
    description: "",
  };

  const updateMainAddress = (patch: Partial<typeof mainAddress>) => {
    const updated = [...addresses];
    updated[0] = { ...mainAddress, ...patch };
    updateField("addresses", updated);
  };

  const updateMainTimezone = (patch: Partial<typeof mainTimezone>) => {
    const updated = [...addresses];
    updated[0] = {
      ...mainAddress,
      timezone: { ...mainTimezone, ...patch },
    };
    updateField("addresses", updated);
  };

  const handleSubmit: React.FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    await onSubmit({ ...user });
  };

  return (
    <form onSubmit={handleSubmit} className="grid gap-3">
      {/* Основна інформація */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <label className="grid gap-1">
          <span className="text-sm text-slate-300">Ім&apos;я *</span>
          <input
            className="input"
            placeholder="Ім&apos;я"
            value={user.first_name}
            onChange={(e) => updateField("first_name", e.target.value)}
            required
          />
        </label>

        <label className="grid gap-1">
          <span className="text-sm text-slate-300">Прізвище *</span>
          <input
            className="input"
            placeholder="Прізвище"
            value={user.last_name}
            onChange={(e) => updateField("last_name", e.target.value)}
            required
          />
        </label>
      </div>

      <label className="grid gap-1">
        <span className="text-sm text-slate-300">Ел. пошта *</span>
        <input
          className="input"
          placeholder="Ел. пошта"
          type="email"
          value={user.email}
          onChange={(e) => updateField("email", e.target.value)}
          required
          />
      </label>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <label className="grid gap-1">
          <span className="text-sm text-slate-300">Телефон</span>
          <input
            className="input"
            placeholder="Телефон"
            type="tel"
            value={user.phone || ""}
            onChange={(e) => updateField("phone", e.target.value)}
          />
        </label>

        <label className="grid gap-1 sm:col-span-2">
          <span className="text-sm text-slate-300">Стать</span>
          <select
            className="select"
            value={user.gender || ""}
            onChange={(e) => updateField("gender", e.target.value as User["gender"])}
          >
            <option value="" disabled selected className="text-slate-300">Оберіть стать</option>
            <option value="male">Чоловіча</option>
            <option value="female">Жіноча</option>
          </select>
        </label>
      </div>

      {/* Основна адреса */}
      <fieldset>
        <legend>Основна адреса</legend>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
          <label className="grid gap-1 sm:col-span-2">
            <span className="text-sm text-slate-300">Вулиця *</span>
            <input
              className="input"
              placeholder="Вулиця"
              value={mainAddress.street || ""}
              onChange={(e) => updateMainAddress({ street: e.target.value })}
              required
            />
          </label>

          <label className="grid gap-1">
            <span className="text-sm text-slate-300">Місто *</span>
            <input
              className="input"
              placeholder="Місто"
              value={mainAddress.city || ""}
              onChange={(e) => updateMainAddress({ city: e.target.value })}
              required
            />
          </label>

          <label className="grid gap-1">
            <span className="text-sm text-slate-300">Країна *</span>
            <input
              className="input"
              placeholder="Країна"
              value={mainAddress.country || ""}
              onChange={(e) => updateMainAddress({ country: e.target.value })}
              required
            />
          </label>
        </div>
      </fieldset>

      {/* Часовий пояс */}
      <fieldset>
        <legend>Часовий пояс</legend>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <label className="grid gap-1">
            <span className="text-sm text-slate-300">Зміщення</span>
            <input
              className="input"
              placeholder="Зміщення (наприклад, +02:00)"
              value={mainTimezone.offset || ""}
              onChange={(e) =>
                updateMainTimezone({ offset: e.target.value })
              }
            />
          </label>

          <label className="grid gap-1 sm:col-span-2">
            <span className="text-sm text-slate-300">Опис</span>
            <input
              className="input"
              placeholder="Опис"
              value={mainTimezone.description || ""}
              onChange={(e) =>
                updateMainTimezone({ description: e.target.value })
              }
            />
          </label>
        </div>
      </fieldset>

      <button className="btn btn-primary w-fit" type="submit">
        {submitText}
      </button>
    </form>
  );
}


