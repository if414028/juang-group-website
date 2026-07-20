"use client";
import { useLanguage } from "@/components/language-provider";
export function LocalizedText({children}:{children:string}) { const {t}=useLanguage(); return <>{t(children)}</>; }
