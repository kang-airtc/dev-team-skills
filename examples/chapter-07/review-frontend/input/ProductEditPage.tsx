'use client'

import axios from 'axios'
import { useState, useEffect } from 'react'
import AdminShell from '@/components/admin/AdminShell'

export default function ProductEditPage({ params }: { params: any }) {
  const [data, setData] = useState(null)
  const [flag, setFlag] = useState(false)

  useEffect(() => {
    axios.get(`/api/products/${params.id}`).then((res) => {
      setData(res.data.data)
    }).catch((err) => {
      console.log('加载失败', err)
    })
  }, [params.id])

  const save = async () => {
    setFlag(true)
    axios.put(`/api/products/${params.id}`, data).then(() => {
      alert('保存成功')
    })
  }

  return (
    <AdminShell title="编辑产品">
      <div style={{ padding: '24px', background: '#f5f5f5' }}>
        <input
          className="border px-3 py-2"
          value={(data as any)?.name || ''}
          onChange={(e) => setData({ ...(data as any), name: e.target.value })}
        />
        <button onClick={save} style={{ color: '#fff', background: '#333' }}>
          保存
        </button>
      </div>
    </AdminShell>
  )
}
