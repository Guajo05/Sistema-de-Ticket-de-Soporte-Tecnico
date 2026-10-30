import { useState } from "react";
import {
  AlertCircle,
  FilePlus2,
  Send,
  ShieldAlert,
  Ticket as TicketIcon,
  User,
  Wrench,
} from "lucide-react";

export default function TicketForm({ urgencias, riesgos, usuarios, tecnicos, onCrear }) {
  const [titulo, setTitulo] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [urgenciaId, setUrgenciaId] = useState("");
  const [riesgoId, setRiesgoId] = useState("");
  const [usuarioId, setUsuarioId] = useState("");
  const [tecnicoId, setTecnicoId] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [mensaje, setMensaje] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setEnviando(true);
    setMensaje(null);
    try {
      const datos = {
        titulo,
        descripcion,
        urgencia_ticket_id: Number(urgenciaId),
        riesgo_ticket_id: Number(riesgoId),
        usuario_id: Number(usuarioId),
      };
      if (tecnicoId) datos.tecnico_id = Number(tecnicoId);

      await onCrear(datos);
      
      setTitulo("");
      setDescripcion("");
      setUrgenciaId("");
      setRiesgoId("");
      setUsuarioId("");
      setTecnicoId("");
      setMensaje({ tipo: "ok", texto: "Ticket creado correctamente" });
    } catch (err) {
      setMensaje({ tipo: "error", texto: err.message });
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h3>
        <TicketIcon size={18} strokeWidth={2.3} />
        Nuevo ticket
      </h3>

      {usuarios.length === 0 && (
        <p className="msg msg-error">
          <AlertCircle size={14} strokeWidth={2.3} />
          Primero crea un usuario (formulario de abajo).
        </p>
      )}

      <label>
        <span className="label-texto">
          <FilePlus2 size={13} strokeWidth={2.3} />
          Título
        </span>
        <input
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
          maxLength={150}
          required
        />
      </label>

      <label>
        <span className="label-texto">
          <FilePlus2 size={13} strokeWidth={2.3} />
          Descripción
        </span>
        <textarea
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
          rows={3}
          required
        />
      </label>

      <label>
        <span className="label-texto">
          <AlertCircle size={13} strokeWidth={2.3} />
          Urgencia
        </span>
        <select value={urgenciaId} onChange={(e) => setUrgenciaId(e.target.value)} required>
          <option value="">Selecciona…</option>
          {urgencias.map((u) => (
            <option key={u.id} value={u.id}>
              {u.nombre}
            </option>
          ))}
        </select>
      </label>

      <label>
        <span className="label-texto">
          <ShieldAlert size={13} strokeWidth={2.3} />
          Riesgo
        </span>
        <select value={riesgoId} onChange={(e) => setRiesgoId(e.target.value)} required>
          <option value="">Selecciona…</option>
          {riesgos.map((r) => (
            <option key={r.id} value={r.id}>
              {r.nombre}
            </option>
          ))}
        </select>
      </label>

      <label>
        <span className="label-texto">
          <User size={13} strokeWidth={2.3} />
          Solicitante
        </span>
        <select value={usuarioId} onChange={(e) => setUsuarioId(e.target.value)} required>
          <option value="">Selecciona…</option>
          {usuarios.map((u) => (
            <option key={u.id} value={u.id}>
              {u.nombre}
              {u.departamento ? ` (${u.departamento})` : ""}
            </option>
          ))}
        </select>
      </label>

      <label>
        <span className="label-texto">
          <Wrench size={13} strokeWidth={2.3} />
          Técnico (opcional)
        </span>
        <select value={tecnicoId} onChange={(e) => setTecnicoId(e.target.value)}>
          <option value="">Sin asignar</option>
          {tecnicos.map((t) => (
            <option key={t.id} value={t.id}>
              {t.nombre}
            </option>
          ))}
        </select>
      </label>

      <button className="btn" type="submit" disabled={enviando}>
        <Send size={15} strokeWidth={2.3} />
        {enviando ? "Creando…" : "Crear ticket"}
      </button>

      {mensaje && (
        <p className={`msg msg-${mensaje.tipo}`}>
          {mensaje.tipo === "ok" ? (
            <FilePlus2 size={14} strokeWidth={2.3} />
          ) : (
            <AlertCircle size={14} strokeWidth={2.3} />
          )}
          {mensaje.texto}
        </p>
      )}
    </form>
  );
}