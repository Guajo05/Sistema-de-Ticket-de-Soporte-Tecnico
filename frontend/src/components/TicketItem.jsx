import {
  AlertCircle,
  AlertTriangle,
  ArrowDownCircle,
  CalendarDays,
  CheckCircle2,
  CheckCheck,
  Clock,
  Flame,
  Loader2,
  Trash2,
  User,
  Wrench,
} from "lucide-react";

// "En progreso" -> "en-progreso", "Crítica" -> "critica" (para las clases CSS)
function slug(texto) {
  return texto
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/\s+/g, "-");
}

// Ícono según urgencia (por texto normalizado)
const ICONO_URGENCIA = {
  baja: ArrowDownCircle,
  media: AlertCircle,
  alta: AlertTriangle,
  critica: Flame,
};

// Ícono según estado (por texto normalizado)
const ICONO_ESTADO = {
  abierto: Clock,
  "en-progreso": Loader2,
  resuelto: CheckCircle2,
  cerrado: CheckCheck,
};

export default function TicketItem({ ticket, estados, tecnicos, onActualizar, onEliminar }) {
  function cambiarEstado(e) {
    onActualizar(ticket.id, { estado_ticket_id: Number(e.target.value) });
  }

  function cambiarTecnico(e) {
    const valor = e.target.value;
    onActualizar(ticket.id, { tecnico_id: valor === "" ? null : Number(valor) });
  }

  function eliminar() {
    if (window.confirm(`¿Eliminar el ticket #${ticket.id} "${ticket.titulo}"?`)) {
      onEliminar(ticket.id);
    }
  }

  const slugUrgencia = slug(ticket.urgencia.nombre);
  const slugEstado = slug(ticket.estado.nombre);

  const IconoUrgencia = ICONO_URGENCIA[slugUrgencia] ?? AlertCircle;
  const IconoEstado = ICONO_ESTADO[slugEstado] ?? Clock;

  return (
    <article className="card ticket">
      <div className="ticket-cabecera">
        <h3>
          <span className="ticket-id">#{ticket.id}</span> {ticket.titulo}
        </h3>
        <div className="badges">
          <span className={`badge urgencia-${slugUrgencia}`}>
            <IconoUrgencia size={13} strokeWidth={2.5} />
            {ticket.urgencia.nombre}
          </span>
          <span className={`badge estado-${slugEstado}`}>
            <IconoEstado size={13} strokeWidth={2.5} />
            {ticket.estado.nombre}
          </span>
        </div>
      </div>

      <p className="ticket-descripcion">{ticket.descripcion}</p>

      <p className="ticket-meta">
        <span className="meta-item">
          <User size={14} strokeWidth={2.2} />
          <strong>{ticket.usuario.nombre}</strong>
          {ticket.usuario.departamento ? ` · ${ticket.usuario.departamento}` : ""}
        </span>
        <span className="meta-item">
          <CalendarDays size={14} strokeWidth={2.2} />
          {new Date(ticket.fecha_creacion).toLocaleString("es-DO")}
        </span>
      </p>

      <div className="acciones">
        <label>
          Estado
          <select value={ticket.estado.id} onChange={cambiarEstado}>
            {estados.map((e) => (
              <option key={e.id} value={e.id}>
                {e.nombre}
              </option>
            ))}
          </select>
        </label>

        <label>
          Técnico
          <select value={ticket.tecnico?.id ?? ""} onChange={cambiarTecnico}>
            <option value="">Sin asignar</option>
            {tecnicos.map((t) => (
              <option key={t.id} value={t.id}>
                {t.nombre}
              </option>
            ))}
          </select>
        </label>

        <button className="btn btn-peligro" type="button" onClick={eliminar}>
          <Trash2 size={16} strokeWidth={2.3} />
          Eliminar
        </button>
      </div>
    </article>
  );
}