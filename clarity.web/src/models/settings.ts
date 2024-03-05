export interface Header {
  title: string
  date_format: string
}

export interface Application {
  title: string
  subtitle: string
  icon: string
  host: string
  href: string
}

export interface Settings {
  header: Header
  apps: Application[]
}

export interface ValidationError {
  type: string
  loc: any[]
  msg: string
  input: Object
  url: string
}
