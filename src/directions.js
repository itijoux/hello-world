// All exploration content lives here. Swap getExplorationDirections() for a
// model call later — the App only needs the same return shape back.

export const profiles = [
  {
    id: "maya",
    name: "Maya",
    grade: "Junior",
    classes: ["AP Biology", "Chemistry", "Studio Art"],
    note: "Dissects on Tuesday, draws from a still life on Thursday.",
  },
  {
    id: "devon",
    name: "Devon",
    grade: "Sophomore",
    classes: ["Algebra II", "Intro to Computer Science", "World History"],
    note: "Likes writing code, likes stories about empires falling.",
  },
  {
    id: "sam",
    name: "Sam",
    grade: "Junior",
    classes: ["English 11", "US History", "General Math", "Earth Science", "PE"],
    note: "No declared focus yet — exploring on purpose.",
  },
];

export function getExplorationDirections(profile) {
  if (profile.id === "maya") {
    return [
      {
        title: "Medical Illustration",
        connection:
          "AP Bio gives you the anatomy; Studio Art gives you the eye. Most of the diagrams in your textbook were drawn by people who do exactly this — and major medical schools still have illustrators on staff.",
        nextStep:
          "Look up the AMI (Association of Medical Illustrators) student gallery tonight. If you can take Anatomy & Physiology next year, that's the on-ramp.",
      },
      {
        title: "Art Conservation",
        connection:
          "When a 400-year-old painting cracks, the person who fixes it is a chemist who can also retouch a Vermeer. Solvent tests in the morning, inpainting in the afternoon — your Chemistry and Studio Art, on the same bench.",
        nextStep:
          "Email the conservation department at the nearest art museum and ask if they ever host high schoolers for an afternoon. The answer is yes more often than you'd guess.",
      },
      {
        title: "Prosthetics & Orthotics Design",
        connection:
          "A well-designed prosthetic limb is sculpture with biomechanics constraints. The observational skills from Studio Art plus the muscle-and-bone knowledge from AP Bio is most of the toolkit.",
        nextStep:
          "Try Blender (free) for a weekend, or ask your art teacher whether there's a 3D modeling or sculpture elective you haven't noticed.",
      },
      {
        title: "Forensic Facial Reconstruction",
        connection:
          "Forensic anthropologists rebuild faces from skulls using tissue-depth markers and a sculptor's hands. The job description is essentially anatomy plus portrait drawing.",
        nextStep:
          "Read one case write-up from the Smithsonian's forensic anthropology team — they publish them publicly. See whether the puzzle of it grabs you.",
      },
      {
        title: "Botanical Illustration & Field Science",
        connection:
          "Every plant species in a herbarium needs an accurate drawing, and labs that study plant chemistry hire illustrators who understand what they're looking at. It's a small field but it's a real one.",
        nextStep:
          "Spend twenty minutes carefully drawing one leaf this week — vein structure, edge shape, where it attaches. Notice whether you find it tedious or quietly absorbing.",
      },
    ];
  }

  if (profile.id === "devon") {
    return [
      {
        title: "Computational History",
        connection:
          "Historians now write code to map slave-ship routes, trace which words appear across 200 years of newspapers, or model how the Black Death actually spread. It's your Intro CS pointed straight at your World History.",
        nextStep:
          "Search 'Stanford Humanities + Design Lab' and pick one project page to read. Most have a two-minute video that shows what the work looks like.",
      },
      {
        title: "Cryptography",
        connection:
          "Breaking Enigma in WWII used math you're about eighteen months from. Modern cryptography sits on number theory and algorithms — Algebra II is the on-ramp, and CS is the lab.",
        nextStep:
          "Try the first three Cryptopals challenges (free, online). If you finish one, you'll want the next.",
      },
      {
        title: "Game Design — Strategy & Simulation",
        connection:
          "Games like Civilization, Crusader Kings, and Europa Universalis are history simulators built by programmers who care about how empires actually worked. CS plus World History is an unusually direct path in.",
        nextStep:
          "For an Intro CS project, build a tiny turn-based map game on a 3×3 grid. That's the genre, scaled down to one weekend.",
      },
      {
        title: "Urban Planning & GIS",
        connection:
          "Cities are math problems with history baked in: why does this street curve, why is the highway here, who got moved out when it was built. GIS software is essentially programming with maps.",
        nextStep:
          "Open QGIS (free) and load any city's open-data shapefile. Twenty minutes of clicking around tells you whether the work feels good.",
      },
      {
        title: "Data Journalism",
        connection:
          "The Pudding, FiveThirtyEight, and the NYT Upshot are newsrooms where reporters write code. Your three classes are unusually well-aimed at this combination.",
        nextStep:
          "Read one Pudding article all the way through, scroll-driven graphics and all. Then ask your CS teacher about learning a bit of Python for data.",
      },
      {
        title: "Computational Linguistics",
        connection:
          "Languages have grammars; grammars are rule systems; rule systems are code. World History gives you the trade routes that pushed languages around, CS gives you the tools to model them.",
        nextStep:
          "If you're taking a language class, ask the teacher how Duolingo decides which words to teach you next. The answer is an algorithm, and you can almost see it.",
      },
    ];
  }

  if (profile.id === "sam") {
    return [
      {
        title: "Generalist Paths (And Why They Pay)",
        connection:
          "You haven't narrowed yet — that's not a hole, it's a skill. Product managers, librarians, consultants, and journalists all get paid to learn a new field fast and then explain it. Specialists envy this.",
        nextStep:
          "Pick a Wikipedia article this week on something you know nothing about. Read it end to end. Repeat next week. That habit is most of the job.",
      },
      {
        title: "Becoming an EMT at 17",
        connection:
          "In most states you can certify as an Emergency Medical Technician at 17 or 18 with a one-semester course. You can be working — paid, in an ambulance or ER — before you graduate.",
        nextStep:
          "Search '[your state] EMT certification minimum age.' The rule is usually one sentence and tells you exactly what to do next.",
      },
      {
        title: "Skilled Trades You Don't Know Exist",
        connection:
          "Electrician, HVAC tech, machinist, welder, elevator mechanic — most pay $70k–$120k mid-career through apprenticeships that pay you while you learn. Your school probably never mentions them.",
        nextStep:
          "Pull up the nearest community college's website and find the 'workforce' or 'trades' page. Just read every program name — some will surprise you.",
      },
      {
        title: "Field Research Assistant",
        connection:
          "Wildlife biologists, archaeologists, and climate scientists hire high-school-aged assistants for summer fieldwork. Often room and board are covered, and the work is outside and real.",
        nextStep:
          "Look up the Student Conservation Association (SCA). Their high-school crews are paid summer jobs in national parks — applications open in winter.",
      },
      {
        title: "Audio — Podcasts, Sound Design, Radio",
        connection:
          "If you can listen carefully and write a clean sentence, you can edit audio. NPR, This American Life, and dozens of independent shows were made by people who did not pick a major at sixteen.",
        nextStep:
          "Install Audacity (free). Record yourself talking for sixty seconds, then cut out every 'um.' That's the entry-level skill, and it takes one evening to try.",
      },
      {
        title: "Library & Archive Work",
        connection:
          "Librarians and archivists are the generalists' generalists — they help researchers find things across every field. The work is calm, the people are curious, and many libraries hire high-school pages.",
        nextStep:
          "Ask your school librarian what an MLIS degree actually involves. Five minutes of that conversation will rearrange what you thought librarians did.",
      },
    ];
  }

  return [];
}
