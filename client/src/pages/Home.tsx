// Design philosophy reminder: Contemporary Pâtisserie Editorial — warm craft, asymmetrical editorial rhythm, tactile product cards, refined Greek content, and subtle pastry-box interactions.
// This page turns the Firecrawl-scraped Le Gateau content and all discovered site photography into a modern single-page patisserie experience.

import { useMemo, useState } from "react";
import { ArrowUpRight, Clock, Instagram, Mail, MapPin, Phone, Sparkles } from "lucide-react";
import {
  allSitePhotos,
  brandAssets,
  categoryRepresentatives,
  contactDetails,
  editorialPhotos,
  generatedAssets,
  productCategories,
} from "@/data/siteData";

type Photo = (typeof allSitePhotos)[number];

const storyParagraphs = [
  "H ιστορία του Le Gateau ξεκίνησε μια Δευτέρα του 2013. Σαν «Πρώτη Ύλη», είχαμε από την αρχή την ιδέα να φτιάχνονται όλα τα προϊόντα από μας.",
  "Η αρχή μας είναι κάθε γλυκό που εκτίθεται στη βιτρίνα μας να είναι ισάξιο με τα υπόλοιπα και να ανακαλύπτεται από το δικό του κοινό.",
  "Στοίχημα για μας είναι να προκαλέσουμε τους φίλους μας να δοκιμάσουν. Βασισμένοι σε αυτές τις «Πρώτες Ύλες» φτιάχνουμε τα γλυκά, τις τούρτες, τα σιροπιαστά, τα κεράσματα, τα αρτοποιήματα και το παγωτό μας.",
];

const fairyQuote =
  "Δεν είναι μόνο πέντε οι αισθήσεις. Υπάρχει και μία έκτη που για να την αισθανθείτε πρέπει να έρθετε στο μαγαζί μας, στο εργαστήρι μας, στην Πόλη του Νερού.";

const logo = brandAssets.find((asset) => asset.title === "Le Gateau")?.src;
const espa = brandAssets.find((asset) => asset.title === "ESPA")?.src;

function categoryTone(category: string) {
  const tones: Record<string, string> = {
    Τούρτες: "from-[#5b2d28]/90 to-[#8d5b52]/80",
    Γάμος: "from-[#72533f]/90 to-[#c9a369]/80",
    Γενέθλια: "from-[#7b2f3d]/90 to-[#c06f80]/80",
    Βάφτιση: "from-[#574a7a]/90 to-[#b8a6d6]/80",
    Πάστες: "from-[#4d2d24]/90 to-[#a15f4b]/80",
    Τάρτες: "from-[#755029]/90 to-[#c8944a]/80",
  };
  return tones[category] ?? "from-[#4b352c]/90 to-[#9b765f]/80";
}

function SectionLabel({ kicker, title, text }: { kicker: string; title: string; text?: string }) {
  return (
    <div className="section-label">
      <span>{kicker}</span>
      <h2>{title}</h2>
      {text ? <p>{text}</p> : null}
    </div>
  );
}

function PhotoCard({ photo, index, compact = false }: { photo: Photo; index: number; compact?: boolean }) {
  return (
    <figure className={`photo-card ${compact ? "photo-card--compact" : ""}`} style={{ animationDelay: `${Math.min(index, 12) * 55}ms` }}>
      <img src={photo.src} alt={`${photo.title} — ${photo.category}`} loading={index < 8 ? "eager" : "lazy"} />
      <figcaption>
        <span>{String(index + 1).padStart(2, "0")}</span>
        <strong>{photo.category}</strong>
      </figcaption>
    </figure>
  );
}

export default function Home() {
  const [activeCategory, setActiveCategory] = useState("Όλες");

  const categories = useMemo(() => ["Όλες", ...Array.from(new Set(allSitePhotos.map((photo) => photo.category)))], []);
  const filteredPhotos = useMemo(
    () => (activeCategory === "Όλες" ? allSitePhotos : allSitePhotos.filter((photo) => photo.category === activeCategory)),
    [activeCategory],
  );

  const heroOriginal = editorialPhotos[0] ?? allSitePhotos[0];
  const storyImages = editorialPhotos.slice(1, 4);

  return (
    <main className="site-shell">
      <nav className="topbar" aria-label="Primary navigation">
        <a className="brand-mark" href="#home" aria-label="Le Gateau home">
          {logo ? <img src={logo} alt="Le Gateau" /> : <span>Le Gateau</span>}
        </a>
        <div className="nav-links">
          <a href="#story">Προφίλ</a>
          <a href="#products">Προϊόντα</a>
          <a href="#gallery">Φωτογραφίες</a>
          <a href="#visit">Επικοινωνία</a>
        </div>
        <a className="nav-call" href={`tel:${contactDetails.phone}`}>
          <Phone size={16} /> {contactDetails.phone}
        </a>
      </nav>

      <section id="home" className="hero-section" style={{ backgroundImage: `linear-gradient(90deg, rgba(41,28,24,.88), rgba(41,28,24,.48), rgba(41,28,24,.12)), url(${generatedAssets.hero})` }}>
        <div className="hero-content">
          <p className="eyebrow">Ζαχαροπλαστείο · Καφέ · Έδεσσα</p>
          <h1>Γλυκά που ανοίγουν όλες τις αισθήσεις.</h1>
          <p>
            Μια πιο σύγχρονη, ζεστή παρουσία για το Le Gateau, βασισμένη στην αρχική ιστορία, στα προϊόντα και στις φωτογραφίες του καταστήματος.
          </p>
          <div className="hero-actions">
            <a className="btn-primary" href="#products">Δείτε τα προϊόντα</a>
            <a className="btn-secondary" href={`mailto:${contactDetails.email}`}>Επικοινωνήστε μαζί μας</a>
          </div>
        </div>
        <aside className="hero-card" aria-label="Le Gateau original photography highlight">
          {heroOriginal ? <img src={heroOriginal.src} alt={`${heroOriginal.title} original Le Gateau photography`} /> : null}
          <div>
            <span>Original site photo</span>
            <strong>{heroOriginal?.category ?? "Le Gateau"}</strong>
          </div>
        </aside>
      </section>

      <section className="quick-info" aria-label="Essential contact details">
        <article>
          <Clock />
          <div>
            <span>Ώρες Λειτουργίας</span>
            <strong>{contactDetails.hoursWeekdays}</strong>
            <small>{contactDetails.hoursWeekend}</small>
          </div>
        </article>
        <article>
          <MapPin />
          <div>
            <span>Βρείτε μας</span>
            <strong>{contactDetails.addressShort}</strong>
            <small>Στοιχεία από την αρχική σελίδα και σελίδα επικοινωνίας.</small>
          </div>
        </article>
        <article>
          <Mail />
          <div>
            <span>Email</span>
            <strong>{contactDetails.email}</strong>
            <small>Για παραγγελίες, εκδηλώσεις και πληροφορίες.</small>
          </div>
        </article>
      </section>

      <section id="story" className="story-section">
        <div className="story-copy">
          <SectionLabel kicker="01 · Προφίλ" title="Το παραμύθι των αισθήσεων" text="Το αρχικό κείμενο του Le Gateau γίνεται μια πιο ευανάγνωστη editorial ιστορία, χωρίς να χάσει τη ζεστασιά του." />
          <blockquote>{fairyQuote}</blockquote>
          {storyParagraphs.map((paragraph) => (
            <p key={paragraph}>{paragraph}</p>
          ))}
          <a className="inline-link" href="#visit">Κλείστε τη δική σας γλυκιά στιγμή <ArrowUpRight size={16} /></a>
        </div>
        <div className="story-collage" aria-label="Original Le Gateau story photos">
          {storyImages.map((photo, index) => (
            <PhotoCard key={photo.src} photo={photo} index={index} compact />
          ))}
        </div>
      </section>

      <img className="flourish" src={generatedAssets.flourish} alt="Decorative patisserie divider" />

      <section id="products" className="products-section">
        <SectionLabel kicker="02 · Προϊόντα" title="Βιτρίνα για κάθε περίσταση" text="Οι κατηγορίες που βρέθηκαν στο αρχικό site παρουσιάζονται σαν σύγχρονο tasting menu, με αυθεντικές φωτογραφίες από το Le Gateau." />
        <div className="category-showcase">
          {categoryRepresentatives.map((photo, index) => {
            const details = productCategories.find((item) => item.name === photo.category);
            return (
              <article className="category-tile" key={`${photo.category}-${photo.src}`}>
                <img src={photo.src} alt={photo.category} loading={index < 4 ? "eager" : "lazy"} />
                <div className={`category-overlay bg-gradient-to-br ${categoryTone(photo.category)}`}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <h3>{photo.category}</h3>
                  <p>{details?.note ?? "Χειροποίητες δημιουργίες Le Gateau"}</p>
                </div>
              </article>
            );
          })}
        </div>
      </section>

      <section className="events-section">
        <div>
          <p className="eyebrow dark">Ανάληψη εκδηλώσεων</p>
          <h2>Γάμοι, βαπτίσεις, γενέθλια και γιορτές με προσωπικό χαρακτήρα.</h2>
        </div>
        <p>
          Το Le Gateau είναι κοντά σας για να ετοιμάσει με υπεύθυνο τρόπο όλες τις σημαντικές εκδηλώσεις, καλύπτοντας τις απαιτήσεις σας σε τούρτες και γλυκά είτε από τα είδη παραγωγής είτε με δικές σας ξεχωριστές προτιμήσεις.
        </p>
      </section>

      <section id="gallery" className="gallery-section">
        <SectionLabel kicker="03 · Φωτογραφίες" title="Όλες οι φωτογραφίες που βρέθηκαν στο site" text={`${allSitePhotos.length} μοναδικές φωτογραφίες προϊόντων και χώρου μεταφέρθηκαν σε σταθερή αποθήκευση και εμφανίζονται εδώ, ώστε καμία φωτογραφία του αρχικού site να μη χαθεί.`} />
        <div className="filter-bar" role="tablist" aria-label="Filter gallery by product category">
          {categories.map((category) => (
            <button
              type="button"
              key={category}
              className={activeCategory === category ? "active" : ""}
              onClick={() => setActiveCategory(category)}
              aria-pressed={activeCategory === category}
            >
              {category}
            </button>
          ))}
        </div>
        <div className="all-gallery">
          {filteredPhotos.map((photo, index) => (
            <PhotoCard key={`${photo.src}-${activeCategory}`} photo={photo} index={index} />
          ))}
        </div>
      </section>

      <section id="visit" className="visit-section">
        <div className="visit-card">
          <p className="eyebrow">04 · Επικοινωνία</p>
          <h2>Περάστε από την Έδεσσα ή μιλήστε μαζί μας.</h2>
          <div className="contact-list">
            <a href={`tel:${contactDetails.phone}`}><Phone size={18} /> {contactDetails.phone}</a>
            <a href={`mailto:${contactDetails.email}`}><Mail size={18} /> {contactDetails.email}</a>
            <a href="https://www.google.com/maps/search/?api=1&query=Le%20Gateau%20Edessa" target="_blank" rel="noreferrer"><MapPin size={18} /> {contactDetails.addressShort}</a>
            <a href={contactDetails.instagram} target="_blank" rel="noreferrer"><Instagram size={18} /> Instagram</a>
          </div>
        </div>
        <div className="visit-panel">
          <Sparkles />
          <h3>Ώρες λειτουργίας</h3>
          <p>{contactDetails.hoursWeekdays}</p>
          <p>{contactDetails.hoursWeekend}</p>
          {espa ? <img src={espa} alt="ESPA" /> : null}
        </div>
      </section>

      <footer className="footer">
        {logo ? <img src={logo} alt="Le Gateau" /> : <strong>Le Gateau</strong>}
        <p>© Le Gateau · Σύγχρονη ανασχεδίαση βασισμένη στο περιεχόμενο και τις φωτογραφίες του αρχικού site.</p>
      </footer>
    </main>
  );
}
