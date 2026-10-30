import { useCallback, useEffect, useState } from "react";
import { Ticket as TicketIcon } from "lucide-react";
import * as api from "./api/tickets";
import PersonaForm from "./components/PersonaForm";
import TicketForm from "./components/TicketForm";
import TicketList from "./components/TicketList";

export default function App() {
  const [estados, setEstados] = useState([]);
  const [urgencias, setUrgencias] = useState([]);
  const [riesgos, setRiesgos] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [tecnicos, setTecnicos] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [filtros, setFiltros] = useState({ estado_id: "", urgencia_id: "" });
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  const cargarCatalogos = useCallback(async () => {
    try {
      const [e, ur, ri, us, te] = await Promise.all([
        api.getEstados(),
        api.getUrgencias(),
        api.getRiesgos(),
        api.getUsuarios(),
        api.getTecnicos(),
      ]);
      setEstados(e);
      setUrgencias(ur);
      setRiesgos(ri);
      setUsuarios(us);
      setTecnicos(te);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  const cargarTickets = useCallback(async () => {
    try {
      const data = await api.getTickets(filtros);
      setTickets(data);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }, [filtros]);

  useEffect(() => {
    cargarCatalogos();
  }, [cargarCatalogos]);

  useEffect(() => {
    cargarTickets();
  }, [cargarTickets]);

  async function crearTicket(datos) {
    await api.crearTicket(datos);
    await cargarTickets();
  }

  async function crearUsuario(datos) {
    await api.crearUsuario(datos);
    setUsuarios(await api.getUsuarios());
  }

  async function crearTecnico(datos) {
    await api.crearTecnico(datos);
    setTecnicos(await api.getTecnicos());
  }

  async function actualizarTicket(id, cambios) {
    try {
      await api.actualizarTicket(id, cambios);
      await cargarTickets();
    } catch (err) {
      setError(err.message);
    }
  }

  async function eliminarTicket(id) {
    try {
      await api.eliminarTicket(id);
      await cargarTickets();
    } catch (err) {
      setError(err.message);
    }
  }

  function cambiarFiltro(clave, valor) {
    setFiltros((previos) => ({ ...previos, [clave]: valor }));
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-contenido">
          <div className="app-header-icono">
            <TicketIcon size={26} strokeWidth={2.2} />
          </div>
          <div>
            <h1>Sistema de Tickets</h1>
            <p>Soporte Técnico · Registra incidencias y dales seguimiento</p>
          </div>
        </div>
      </header>

      {error && (
        <div className="alerta" role="alert">
          <span>{error}</span>
          <button type="button" onClick={() => setError("")} aria-label="Cerrar">
            ×
          </button>
        </div>
      )}

      <main className="layout">
        <aside className="panel-lateral">
          <TicketForm
            urgencias={urgencias}
            riesgos={riesgos}
            usuarios={usuarios}
            tecnicos={tecnicos}
            onCrear={crearTicket}
          />
          <PersonaForm tipo="usuario" onCrear={crearUsuario} />
          <PersonaForm tipo="tecnico" onCrear={crearTecnico} />
        </aside>

        <section className="panel-principal">
          <div className="barra-filtros">
            <h2>Tickets ({tickets.length})</h2>
            <div className="filtros">
              <select
                value={filtros.estado_id}
                onChange={(e) => cambiarFiltro("estado_id", e.target.value)}
              >
                <option value="">Todos los estados</option>
                {estados.map((e) => (
                  <option key={e.id} value={e.id}>{e.nombre}</option>
                ))}
              </select>

              <select
                value={filtros.urgencia_id}
                onChange={(e) => cambiarFiltro("urgencia_id", e.target.value)}
              >
                <option value="">Todas las urgencias</option>
                {urgencias.map((u) => (
                  <option key={u.id} value={u.id}>{u.nombre}</option>
                ))}
              </select>
            </div>
          </div>

          <TicketList
            tickets={tickets}
            cargando={cargando}
            estados={estados}
            tecnicos={tecnicos}
            onActualizar={actualizarTicket}
            onEliminar={eliminarTicket}
          />
        </section>
      </main>
    </div>
  );
}