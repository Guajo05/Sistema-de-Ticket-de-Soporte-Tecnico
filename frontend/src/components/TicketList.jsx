import TicketItem from "./TicketItem";

export default function TicketList({
  tickets,
  cargando,
  estados,
  tecnicos,
  onActualizar,
  onEliminar,
}) {
  if (cargando) return <p className="vacio">Cargando tickets…</p>;
  if (tickets.length === 0) return <p className="vacio">No hay tickets para mostrar.</p>;

  return (
    <div className="lista">
      {tickets.map((t) => (
        <TicketItem
          key={t.id}
          ticket={t}
          estados={estados}
          tecnicos={tecnicos}
          onActualizar={onActualizar}
          onEliminar={onEliminar}
        />
      ))}
    </div>
  );
}