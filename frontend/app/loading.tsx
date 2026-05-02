export default function Loading() {
  return (
    <main>
      <section className="card skeleton">
        <div className="skeletonLine w40" />
        <div className="skeletonLine w90" />
        <div className="skeletonLine w60" />
      </section>
      <section className="grid">
        {[0, 1, 2].map((idx) => (
          <article key={idx} className="card skeleton">
            <div className="skeletonLine w35" />
            <div className="skeletonLine w80" />
            <div className="skeletonLine w70" />
            <div className="skeletonLine w50" />
          </article>
        ))}
      </section>
    </main>
  );
}
