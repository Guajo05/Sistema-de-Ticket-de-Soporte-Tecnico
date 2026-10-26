import { useState } from "react";
import {
  AlertCircle,
  Building2,
  CheckCircle2,
  Mail,
  Send,
  Star,
  User,
  UserPlus,
  Wrench,
} from "lucide-react";

const CONFIG = {
  usuario: {
    titulo: "Nuevo usuario",
    icono: UserPlus,
    campoExtra: "departamento",
    etiquetaExtra: "Departamento",
    iconoExtra: Building2,
  },
  tecnico: {
    titulo: "Nuevo técnico",
    icono: Wrench,
    campoExtra: "especialidad",
    etiquetaExtra: "Especialidad",
    iconoExtra: Star,
  },
};

export default function PersonaForm({ tipo, onCrear }) {
  const cfg = CONFIG[tipo];
  const IconoTitulo = cfg.icono;
  const IconoExtra = cfg.iconoExtra;

  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [extra, setExtra] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [mensaje, setMensaje] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setEnviando(true);
    setMensaje(null);
    try {
      const datos = { nombre, correo };
      if (extra.trim()) datos[cfg.campoExtra] = extra;
      await onCrear(datos);
      setNombre("");
      setCorreo("");
      setExtra("");
      setMensaje({ tipo: "ok", texto: "Creado correctamente" });
    } catch (err) {
      setMensaje({ tipo: "error", texto: err.message });
    } finally {
      setEnviando(false);
    }
  }

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h3>
        <IconoTitulo size={18} strokeWidth={2.3} />
        {cfg.titulo}
      </h3>

      <label>
        <span className="label-texto">
          <User size={13} strokeWidth={2.3} />
          Nombre
        </span>
        <input
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          maxLength={100}
          required
        />
      </label>

      <label>
        <span className="label-texto">
          <Mail size={13} strokeWidth={2.3} />
          Correo
        </span>
        <input
          type="email"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          maxLength={150}
          required
        />
      </label>

      <label>
        <span className="label-texto">
          <IconoExtra size={13} strokeWidth={2.3} />
          {cfg.etiquetaExtra} (opcional)
        </span>
        <input value={extra} onChange={(e) => setExtra(e.target.value)} maxLength={100} />
      </label>

      <button className="btn" type="submit" disabled={enviando}>
        <Send size={15} strokeWidth={2.3} />
        {enviando ? "Guardando…" : "Guardar"}
      </button>

      {mensaje && (
        <p className={`msg msg-${mensaje.tipo}`}>
          {mensaje.tipo === "ok" ? (
            <CheckCircle2 size={14} strokeWidth={2.3} />
          ) : (
            <AlertCircle size={14} strokeWidth={2.3} />
          )}
          {mensaje.texto}
        </p>
      )}
    </form>
  );
}