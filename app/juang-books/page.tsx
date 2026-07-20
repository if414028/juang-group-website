import type { Metadata } from "next";
import { UnderDevelopmentPage } from "@/components/under-development";
export const metadata: Metadata = { title: "Juang Books — In Development", description: "An upcoming Juang Group concept focused on ideas, stories, creativity, and meaningful learning." };
export default function Page() { return <UnderDevelopmentPage name="Juang Books" symbol="JB" image="/images/juang-books/concept-books.webp" imageAlt="Editorial illustration of open books unfolding into paths, leaves, and ideas" description="Juang Books is an upcoming Juang Group concept focused on ideas, stories, creativity, and meaningful learning experiences." />; }
