import React from 'react'

interface Props {
  className?: string
}

export default function Logo({ className = '' }: Props) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <svg
        width="22"
        height="22"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden
      >
        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="1.6" />
        <path
          d="M7.5 13.5C9.5 11 12 9.5 14.5 9.5C16.5 9.5 17.5 11 17 13"
          stroke="currentColor"
          strokeWidth="1.6"
          strokeLinecap="round"
        />
      </svg>
      <span className="text-[17px] font-semibold tracking-tight text-ink">
        某某科技
      </span>
    </div>
  )
}
