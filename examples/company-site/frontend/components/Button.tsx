import React from 'react'

type Variant = 'primary' | 'secondary' | 'ghost' | 'link'
type Size = 'sm' | 'md' | 'lg'

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant
  size?: Size
  asChild?: boolean
}

const variantClasses: Record<Variant, string> = {
  primary:
    'bg-ink text-white hover:bg-neutral-800 focus-visible:ring-ink',
  secondary:
    'bg-surface-alt text-ink hover:bg-neutral-200 focus-visible:ring-ink',
  ghost:
    'bg-transparent text-ink hover:bg-surface-alt focus-visible:ring-ink',
  link:
    'bg-transparent text-ink underline-offset-4 hover:underline focus-visible:ring-ink px-0',
}

const sizeClasses: Record<Size, string> = {
  sm: 'h-9 px-4 text-sm',
  md: 'h-11 px-6 text-[15px]',
  lg: 'h-12 px-8 text-base',
}

export default function Button({
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  ...rest
}: Props) {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-full font-medium ' +
    'transition-colors duration-200 ease-smooth cursor-pointer ' +
    'focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 ' +
    'disabled:opacity-50 disabled:cursor-not-allowed'
  return (
    <button
      className={`${base} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...rest}
    >
      {children}
    </button>
  )
}
