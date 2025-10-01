FROM node:20 AS base

ARG NEXT_PUBLIC_NAME
ENV NEXT_PUBLIC_NAME=$NEXT_PUBLIC_NAME

FROM base AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
# RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* tsconfig.json next.config.ts ./
RUN \
    if [ -f package-lock.json ]; then npm ci; \
    else echo "Lockfile not found." && npm install; \
    fi


FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]