export interface BusinessUnit {
  name: string;
  slug: string;
  status: "featured" | "in-development";
  shortDescription: string;
  href: string;
  mark: string;
}

export const navigation = [
  { label: "Home", href: "/" }, { label: "About", href: "/about" },
  { label: "Yeshua Cafe", href: "/yeshua-cafe" }, { label: "Juang Ice Cream", href: "/juang-ice-cream" },
  { label: "Juang Books", href: "/juang-books" }, { label: "Contact", href: "/contact" },
];

export const businessUnits: BusinessUnit[] = [
  { name: "Yeshua Cafe", slug: "yeshua-cafe", status: "featured", shortDescription: "Justin Juang’s inclusive hospitality brand, growing across Jakarta and Indonesia while creating meaningful roles for people with Down syndrome.", href: "/yeshua-cafe", mark: "01" },
  { name: "Juang Ice Cream", slug: "juang-ice-cream", status: "in-development", shortDescription: "Part of the group’s growing food and beverage portfolio, inspired by joyful flavors and shared experiences.", href: "/juang-ice-cream", mark: "02" },
  { name: "Juang Books", slug: "juang-books", status: "in-development", shortDescription: "A future lifestyle concept focused on ideas, stories, creativity, and meaningful learning.", href: "/juang-books", mark: "03" },
];

export const values = [
  { title: "Entrepreneurial Ambition", description: "Building recognizable brands with the discipline and confidence to expand." },
  { title: "African–Indonesian Connection", description: "Creating commercial bridges between markets, cultures, and opportunities." },
  { title: "Inclusive Opportunity", description: "Opening meaningful participation while respecting ability, dignity, and potential." },
  { title: "Hospitality Excellence", description: "Creating welcoming experiences with quality, relevance, and strong execution." },
  { title: "Portfolio Growth", description: "Expanding from hospitality into consumer products, trading, investment, and new industries." },
  { title: "Lasting Impact", description: "Growing responsibly while creating value for customers, communities, partners, and investors." },
];

export const contactInformation = { email: "", phone: "", whatsapp: "", instagram: "", address: "" };
