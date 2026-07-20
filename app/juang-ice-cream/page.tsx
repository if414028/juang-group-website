import type { Metadata } from "next";
import { UnderDevelopmentPage } from "@/components/under-development";
export const metadata: Metadata = { title: "Juang Ice Cream — In Development", description: "A future Juang Group concept exploring joyful flavors, cultural inspiration, and shared experiences." };
export default function Page() { return <UnderDevelopmentPage name="Juang Ice Cream" symbol="JI" image="/images/juang-ice-cream/concept-still-life.webp" imageAlt="Editorial still life of sculptural ice cream and layered cultural patterns" description="A new concept from Juang Group is being carefully developed. Juang Ice Cream will explore joyful flavors, cultural inspiration, and shared experiences." />; }
