import React from 'react'

interface Props {
  eyebrow?: string
  title: string
  description?: string
  align?: 'left' | 'center'
}

export default function SectionHeader({
  eyebrow,
  title,
  description,
  align = 'left',
}: Props) {
  const alignClass = align === 'center' ? 'text-center mx-auto' : 'text-left'
  return (
    <div className={`max-w-3xl ${alignClass}`}>
      {eyebrow && (
        <div className="text-sm font-medium text-ink-muted uppercase tracking-wider mb-3">
          {eyebrow}
        </div>
      )}
      <h2 className="text-3xl md:text-5xl font-semibold tracking-tightest text-ink leading-[1.05]">
        {title}
      </h2>
      {description && (
        <p className="mt-4 text-base md:text-lg text-ink-muted leading-relaxed">
          {description}
        </p>
      )}
    </div>
  )
}
