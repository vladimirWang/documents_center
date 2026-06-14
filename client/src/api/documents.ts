export type DocumentType = 'pdf' | 'doc' | 'sheet' | 'image' | 'note'

export interface DocumentItem {
  id: string
  title: string
  type: DocumentType
  updatedAt: string
  summary: string
  content: string
}

const mockDocuments: DocumentItem[] = [
  {
    id: '1',
    title: '2026 年度产品规划',
    type: 'pdf',
    updatedAt: '2026-06-12',
    summary: '包含 Q3/Q4 产品路线图与里程碑。',
    content:
      '本文档概述了 2026 年下半年产品规划，涵盖核心功能迭代、用户体验优化以及商业化路径。重点包括文档协作、权限管理与多端同步能力。',
  },
  {
    id: '2',
    title: '技术架构评审纪要',
    type: 'doc',
    updatedAt: '2026-06-10',
    summary: '微服务拆分与 API 网关方案讨论记录。',
    content:
      '评审会议确认了前后端分离架构，后端采用 FastAPI，前端使用 React + Vite。鉴权统一走 JWT，文档服务后续接入对象存储。',
  },
  {
    id: '3',
    title: '运营数据周报',
    type: 'sheet',
    updatedAt: '2026-06-08',
    summary: '本周新增用户、活跃与留存指标汇总。',
    content:
      '本周 DAU 增长 12%，文档创建量提升 8%。渠道投放 ROI 稳定，建议继续优化 onboarding 流程。',
  },
  {
    id: '4',
    title: '品牌视觉规范',
    type: 'image',
    updatedAt: '2026-06-05',
    summary: 'Logo、配色与图标使用规范。',
    content:
      '主色建议使用品牌蓝 #3182CE，辅助色为灰阶体系。图标统一使用线性风格，保证在浅色与深色背景下可读。',
  },
  {
    id: '5',
    title: '会议纪要 - 需求评审',
    type: 'note',
    updatedAt: '2026-06-01',
    summary: '登录、文档列表与详情页需求确认。',
    content:
      '已确认 MVP 包含登录、首页入口、我的文档列表与文档详情。首页暂用 mock 图标数据，文档接口待后端提供后切换为真实 API。',
  },
]

export const fetchDocuments = async (): Promise<DocumentItem[]> => {
  await new Promise((resolve) => setTimeout(resolve, 300))
  return mockDocuments
}

export const fetchDocumentById = async (id: string): Promise<DocumentItem | null> => {
  await new Promise((resolve) => setTimeout(resolve, 200))
  return mockDocuments.find((doc) => doc.id === id) ?? null
}
