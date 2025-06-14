# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
Please respond in Japanese.

## Project Overview

This is the Japanese localization of the JHipster official website (https://www.jhipster.tech/jp/), built with Docusaurus. It serves as a translation and localization fork of the main JHipster website repository.

## Development Commands

### Basic Commands
- `npm install` - Install dependencies
- `npm start` - Start local development server (auto-reloads on changes)
- `npm run build` - Build static site for production in `build/` directory
- `npm run serve` - Serve the production build locally
- `npm run typecheck` - Run TypeScript type checking
- `npm run clear` - Clear Docusaurus cache

### Development Workflow
- `npm run write-translations` - Generate translation files
- `npm run write-heading-ids` - Generate heading IDs for docs
- `npm run analyze` - Build with bundle analyzer

## Architecture

### Core Structure
- **Docusaurus-based**: Uses Docusaurus v3 as the static site generator
- **TypeScript + React**: Component-based architecture with TypeScript
- **Bilingual**: Supports Japanese (default) and English locales
- **MDX Documentation**: All documentation is in MDX format in the `docs/` directory

### Key Directories
- `docs/` - Main documentation content in MDX format, organized by categories
- `src/components/` - React components organized by feature (sections, ui, etc.)
- `src/pages/` - Custom pages (team, modules, etc.)
- `src/theme/` - Docusaurus theme customizations
- `static/` - Static assets (images, logos, etc.)
- `pages/` - Legacy markdown pages

### Component Organization
Components are organized by domain:
- `sections/` - Main page sections (welcome, marketplace, team, docs)
- `ui/` - Reusable UI components (Carousel, Input, SectionWrapper)
- Theme customizations extend Docusaurus default components

### Localization Architecture
- Primary locale: Japanese (`ja`)
- Secondary locale: English (`en`)
- Content structure supports both languages through Docusaurus i18n
- Base URL is `/jp/` for Japanese site deployment

## Translation Workflow

This repository follows a sophisticated upstream synchronization process:
1. GitHub Actions monitors the upstream JHipster repository
2. Creates sync branches with translation markers when updates are detected
3. Translators resolve conflicts and translate new content
4. Changes are merged to main branch

## Deployment

### GitHub Pages Deployment
- Automatic deployment on pushes to `main` branch
- Production site: https://www.jhipster.tech/jp/
- Deployment target: `gh-pages` branch
- Note: `gh-pages` branch has slight differences from `main` for Japanese site functionality

### Build Process
- Node.js 20+ required
- TypeScript compilation
- Docusaurus static generation
- SCSS compilation for styling

## Configuration

### Key Config Files
- `docusaurus.config.ts` - Main Docusaurus configuration
- `sidebars.ts` - Documentation sidebar structure
- `redirects.config.ts` - URL redirects configuration
- `tsconfig.json` - TypeScript configuration (extends Docusaurus defaults)

### Content Management
- Japanese translations utilize TexTra® automatic translation as base
- Documentation follows specific style guidelines for consistency
- Regular synchronization with upstream JHipster documentation

## Testing

- `npm run build` validates the build process
- GitHub Actions run deployment tests on PRs
- TypeScript checking ensures type safety

## 機能改善：日本語ドキュメント自動翻訳

自動翻訳システムは`.github/auto-translation`ディレクトリ内で完結して管理されています。

### 自動翻訳システムの構成
- **仕様書**: `.github/auto-translation/spec.md`
- **タスク一覧**: `.github/auto-translation/tasks.md`
- **実装**: `.github/auto-translation/scripts/`内のPythonスクリプト
- **テスト**: `.github/auto-translation/tests/`
- **設定**: `.github/auto-translation/pyproject.toml`、`.github/auto-translation/Makefile`

### 自動翻訳システムの実行方法
```bash
# 自動翻訳ディレクトリに移動
cd .github/auto-translation

# 環境セットアップ
make dev-setup

# テスト実行
make test

# 翻訳実行（ドライラン）
make run-dry
```

この設計により、メインプロジェクトのファイル構成に影響を与えずに自動翻訳機能を管理できます。
