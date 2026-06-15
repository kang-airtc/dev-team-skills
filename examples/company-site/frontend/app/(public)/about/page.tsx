import Container from '@/components/Container'
import SectionHeader from '@/components/SectionHeader'

export default function AboutPage() {
  return (
    <div>
      <section className="pt-24 md:pt-32 pb-20 bg-gradient-to-b from-surface-alt to-white">
        <Container>
          <div className="max-w-3xl">
            <div className="text-sm font-medium text-ink-muted uppercase tracking-wider mb-4">
              About
            </div>
            <h1 className="text-5xl md:text-7xl font-semibold tracking-tightest text-ink leading-[1.02]">
              工艺、直觉、
              <br />
              与对细节的偏执。
            </h1>
            <p className="mt-6 text-lg md:text-xl text-ink-muted leading-relaxed">
              我们相信，最好的科技，是被忘记的科技。
              它静静存在，让你专注于真正重要的事。
            </p>
          </div>
        </Container>
      </section>

      <section className="py-20 md:py-28">
        <Container>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                title: '设计驱动',
                desc: '从一颗螺丝到整机比例，每个细节都被反复推敲。',
              },
              {
                title: '工艺至上',
                desc: 'CNC 一体成型机身、双面纳米玻璃、航空级合金。',
              },
              {
                title: '生态协同',
                desc: '设备之间无缝接力，让工作与生活自由切换。',
              },
            ].map((it) => (
              <div
                key={it.title}
                className="rounded-3xl bg-surface-alt p-10"
              >
                <div className="text-2xl font-semibold tracking-tight text-ink mb-3">
                  {it.title}
                </div>
                <p className="text-ink-muted leading-relaxed">{it.desc}</p>
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section className="py-20 md:py-28 bg-surface-alt">
        <Container>
          <SectionHeader eyebrow="Numbers" title="数字背后" />
          <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { num: '10+', label: '年专注研发' },
              { num: '120M', label: '全球用户' },
              { num: '60+', label: '国家与地区' },
              { num: '4.9', label: '用户口碑均分' },
            ].map((s) => (
              <div key={s.label} className="rounded-2xl bg-white p-8 border border-line">
                <div className="text-4xl md:text-5xl font-semibold tracking-tightest text-ink">
                  {s.num}
                </div>
                <div className="mt-2 text-sm text-ink-muted">{s.label}</div>
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section className="py-20 md:py-28">
        <Container size="narrow">
          <SectionHeader
            eyebrow="Mission"
            title="我们的使命"
            description="把复杂留给自己，把简单留给用户。让每一次握持、每一次开机，都成为一次愉悦的体验。"
            align="center"
          />
        </Container>
      </section>
    </div>
  )
}
