import React from 'react'

interface Props {
  children: React.ReactNode
  className?: string
  size?: 'default' | 'wide' | 'narrow'
}

export default function Container({ children, className = '', size = 'default' }: Props) {
  const max =
    size === 'wide' ? 'max-w-7xl' : size === 'narrow' ? 'max-w-4xl' : 'max-w-6xl'
  return (
    <div className={`${max} mx-auto px-6 md:px-8 ${className}`}>{children}</div>
  )
}
