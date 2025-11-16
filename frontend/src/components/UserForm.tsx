import { useEffect, useState } from "react";
import type { User } from "../interfaces";

type Props = {
  initial: User;
  onSubmit: (u: User) => Promise<void> | void;
  submitText?: string;
};

export default function UserForm({ initial, onSubmit, submitText = "Зберегти" }: Props) {
  const [user, setUser] = useState<User>(initial);
  useEffect(() => {
    setUser(initial);
  }, [initial]);
  const update = (key: keyof User, value: any) => setUser({ ...user, [key]: value });

  return (
    <form
      onSubmit={async (e) => {
        e.preventDefault();
        const payload: User = { ...user };
        await onSubmit(payload);
      }}
      className="grid gap-3"
    >
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <label className="grid gap-1">
          <span className="text-sm text-slate-300">Ім&apos;я</span>
          <input
            className="input"
            placeholder="Ім&apos;я"
            value={user.first_name}
            onChange={(e) => update("first_name", e.target.value)}
          />
        </label>
        <label className="grid gap-1">
          <span className="text-sm text-slate-300">Прізвище</span>
          <input
            className="input"
            placeholder="Прізвище"
            value={user.last_name}
            onChange={(e) => update("last_name", e.target.value)}
          />
        </label>
      </div>
      <label className="grid gap-1">
        <span className="text-sm text-slate-300">Ел. пошта</span>
        <input className="input" placeholder="Ел. пошта" value={user.email} onChange={(e) => update("email", e.target.value)} />
      </label>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <label className="grid gap-1">
          <span className="text-sm text-slate-300">Телефон</span>
          <input className="input" placeholder="Телефон" value={user.phone || ""} onChange={(e) => update("phone", e.target.value)} />
        </label>
        <label className="grid gap-1 sm:col-span-2">
          <span className="text-sm text-slate-300">Стать</span>
          <select className="select" value={user.gender || ""} onChange={(e) => update("gender", e.target.value)}>
            <option value="">Оберіть стать</option>
            <option value="male">Чоловіча</option>
            <option value="female">Жіноча</option>
          </select>
        </label>
      </div>
      <fieldset>
        <legend>Основна адреса</legend>
        {user.addresses.length === 0 && (
          <></>
        )}
        {/** Ensure we display first address fields even if not present yet */}
        {(() => {
          const addr0 =
            user.addresses[0] ?? ({ street: "", city: "", country: "" } as any);
          return (
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
          <label className="grid gap-1 sm:col-span-2">
            <span className="text-sm text-slate-300">Вулиця</span>
            <input
              className="input"
              placeholder="Вулиця"
              value={addr0.street || ""}
              onChange={(e) => {
                const a = [...(user.addresses ?? [])];
                a[0] = { ...(a[0] ?? {}), street: e.target.value };
                update("addresses", a);
              }}
            />
          </label>
          <label className="grid gap-1">
            <span className="text-sm text-slate-300">Місто</span>
            <input
              className="input"
              placeholder="Місто"
              value={addr0.city || ""}
              onChange={(e) => {
                const a = [...(user.addresses ?? [])];
                a[0] = { ...(a[0] ?? {}), city: e.target.value };
                update("addresses", a);
              }}
            />
          </label>
          <label className="grid gap-1">
            <span className="text-sm text-slate-300">Країна</span>
            <input
              className="input"
              placeholder="Країна"
              value={addr0.country || ""}
              onChange={(e) => {
                const a = [...(user.addresses ?? [])];
                a[0] = { ...(a[0] ?? {}), country: e.target.value };
                update("addresses", a);
              }}
            />
          </label>
        </div>
          );
        })()}
      </fieldset>
      <fieldset>
        <legend>Часовий пояс</legend>
        {(() => {
          const a = [...(user.addresses ?? [])];
          const tz = (a[0] as any)?.timezone ?? { offset: "", description: "" };
          return (
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <label className="grid gap-1">
                <span className="text-sm text-slate-300">Зміщення</span>
                <input
                  className="input"
                  placeholder="Зміщення (наприклад, +02:00)"
                  value={tz.offset || ""}
                  onChange={(e) => {
                    a[0] = { ...(a[0] ?? {}), timezone: { ...tz, offset: e.target.value } };
                    update("addresses", a);
                  }}
                />
              </label>
              <label className="grid gap-1 sm:col-span-2">
                <span className="text-sm text-slate-300">Опис</span>
                <input
                  className="input"
                  placeholder="Опис"
                  value={tz.description || ""}
                  onChange={(e) => {
                    a[0] = {
                      ...(a[0] ?? {}),
                      timezone: { ...tz, description: e.target.value },
                    };
                    update("addresses", a);
                  }}
                />
              </label>
            </div>
          );
        })()}
      </fieldset>
      <button className="btn btn-primary w-fit" type="submit">{submitText}</button>
    </form>
  );
}


