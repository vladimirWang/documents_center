import { Box, Card, Heading, SimpleGrid, Text } from '@chakra-ui/react'
import type { IconType } from 'react-icons'
import {
  FaChartBar,
  FaClipboardList,
  FaCloudUploadAlt,
  FaFileAlt,
  FaFolderOpen,
  FaImage,
  FaRegStar,
  FaUsers,
} from 'react-icons/fa'
import { useNavigate } from 'react-router-dom'

interface QuickEntry {
  id: string
  title: string
  description: string
  icon: IconType
  color: string
  bg: string
  path?: string
}

const quickEntries: QuickEntry[] = [
  {
    id: 'recent',
    title: '最近文档',
    description: '快速查看最近编辑的文件',
    icon: FaFileAlt,
    color: 'blue.500',
    bg: 'blue.50',
    path: '/documents',
  },
  {
    id: 'folders',
    title: '我的文件夹',
    description: '按目录整理你的资料',
    icon: FaFolderOpen,
    color: 'orange.500',
    bg: 'orange.50',
    path: '/documents',
  },
  {
    id: 'upload',
    title: '上传文档',
    description: '支持 PDF、Word、图片等格式',
    icon: FaCloudUploadAlt,
    color: 'green.500',
    bg: 'green.50',
    path: '/files',
  },
  {
    id: 'shared',
    title: '共享给我',
    description: '团队成员分享的文档',
    icon: FaUsers,
    color: 'purple.500',
    bg: 'purple.50',
  },
  {
    id: 'favorites',
    title: '收藏夹',
    description: '标记重要的文档',
    icon: FaRegStar,
    color: 'yellow.500',
    bg: 'yellow.50',
  },
  {
    id: 'reports',
    title: '数据报表',
    description: '运营与业务分析文档',
    icon: FaChartBar,
    color: 'teal.500',
    bg: 'teal.50',
  },
  {
    id: 'templates',
    title: '模板库',
    description: '会议纪要、周报等模板',
    icon: FaClipboardList,
    color: 'pink.500',
    bg: 'pink.50',
  },
  {
    id: 'media',
    title: '图片素材',
    description: '品牌与营销视觉资源',
    icon: FaImage,
    color: 'cyan.500',
    bg: 'cyan.50',
  },
]

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <Box>
      <Heading size="lg" mb={2}>
        欢迎回来
      </Heading>
      <Text color="gray.600" mb={8}>
        从下方快捷入口开始管理你的文档
      </Text>

      <SimpleGrid columns={{ base: 1, sm: 2, md: 3, lg: 4 }} gap={5}>
        {quickEntries.map((entry) => {
          const Icon = entry.icon
          return (
            <Card.Root
              key={entry.id}
              cursor={entry.path ? 'pointer' : 'default'}
              transition="all 0.2s"
              _hover={entry.path ? { shadow: 'md', transform: 'translateY(-2px)' } : undefined}
              onClick={() => entry.path && navigate(entry.path)}
            >
              <Card.Body>
                <Box
                  w={12}
                  h={12}
                  borderRadius="lg"
                  bg={entry.bg}
                  color={entry.color}
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  mb={4}
                  fontSize="xl"
                >
                  <Icon />
                </Box>
                <Heading size="sm" mb={2}>
                  {entry.title}
                </Heading>
                <Text fontSize="sm" color="gray.600">
                  {entry.description}
                </Text>
              </Card.Body>
            </Card.Root>
          )
        })}
      </SimpleGrid>
    </Box>
  )
}
