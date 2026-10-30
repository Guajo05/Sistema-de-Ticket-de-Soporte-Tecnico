const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  let res;
  try {
    res = await fetch(`${API_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error("No se pudo conectar con el servidor. ¿Está corriendo el backend?");
  }

  if (!res.ok) {
    let detalle = `Error ${res.status}`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") {
        detalle = body.detail;
      } else if (Array.isArray(body.detail)) {
        detalle = body.detail.map((d) => d.msg).join(". ");
      }
    } catch {
    }
    throw new Error(detalle);
  }

  if (res.status === 204) return null;
  return res.json();
}

// ---------- Catálogos ----------
export const getEstados = () => request("/estados");
export const getUrgencias = () => request("/urgencias");
export const getRiesgos = () => request("/riesgos");

// ---------- Usuarios y técnicos ----------
export const getUsuarios = () => request("/usuarios");
export const crearUsuario = (datos) =>
  request("/usuarios", { method: "POST", body: JSON.stringify(datos) });

export const getTecnicos = () => request("/tecnicos");
export const crearTecnico = (datos) =>
  request("/tecnicos", { method: "POST", body: JSON.stringify(datos) });

// ---------- Tickets ----------
export function getTickets(filtros = {}) {
  const params = new URLSearchParams();
  Object.entries(filtros).forEach(([clave, valor]) => {
    if (valor !== "" && valor != null) params.append(clave, valor);
  });
  const query = params.toString();
  return request(`/tickets${query ? `?${query}` : ""}`);
}

export const crearTicket = (datos) =>
  request("/tickets", { method: "POST", body: JSON.stringify(datos) });

export const actualizarTicket = (id, cambios) =>
  request(`/tickets/${id}`, { method: "PATCH", body: JSON.stringify(cambios) });

export const eliminarTicket = (id) => request(`/tickets/${id}`, { method: "DELETE" });
