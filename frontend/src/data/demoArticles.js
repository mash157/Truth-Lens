/**
 * Demo Article Library for TruthLens
 *
 * 14 articles total: 5 genuine, 5 fake, 4 ambiguous
 *
 * These are the official DEMO/TESTING set.
 * Source label: "DEMO TEST"
 * Do NOT mix these articles into model evaluation metrics.
 * Expected labels are testing expectations and are not proof of factual truth.
 */

export const DEMO_ARTICLES = [
  // ──────────────────────────────────────────────
  //  GENUINE — 5 examples
  // ──────────────────────────────────────────────
  {
    id: 'genuine-01',
    category: 'International Politics',
    headline: 'China says resolutely opposes deployment of THAAD in South Korea',
    text: 'BEIJING (Reuters) - China said on Friday it resolutely opposes deployment of a U.S. anti-missile defense system in South Korea after South Korea said the system was needed to protect against North Korean missile threats.',
    expectedLabel: 'LIKELY_GENUINE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Genuine',
  },
  {
    id: 'genuine-02',
    category: 'U.S. Politics',
    headline: 'Trump says he will discuss Islamic State fight in two weeks',
    text: 'WASHINGTON (Reuters) - U.S. President Donald Trump said on Monday that he planned to hold a news conference in two weeks to discuss the U.S.-led campaign against Islamic State.',
    expectedLabel: 'LIKELY_GENUINE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Genuine',
  },
  {
    id: 'genuine-03',
    category: 'International Relations',
    headline: "Netanyahu sees U.S.-Israel ties 'reaching new heights' after Trump victory",
    text: "JERUSALEM (Reuters) - Prime Minister Benjamin Netanyahu expressed confidence that relations between Israel and the United States would reach new heights following Donald Trump's election victory.",
    expectedLabel: 'LIKELY_GENUINE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Genuine',
  },
  {
    id: 'genuine-04',
    category: 'Government',
    headline: 'Senate Intelligence committee leaders confirm Kushner testimony',
    text: 'The Republican and Democratic leaders of the Senate Intelligence Committee said on Monday that Jared Kushner would provide testimony to the committee as part of its investigation.',
    expectedLabel: 'LIKELY_GENUINE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Genuine',
  },
  {
    id: 'genuine-05',
    category: 'Natural Disaster',
    headline: "Iran's quake death toll rises to 530, more than 8,000 injured",
    text: "ANKARA (Reuters) - At least 530 people were killed in Iran's deadliest earthquake in more than a decade, state news agency IRNA reported on Tuesday, adding that more than 8,000 people were injured.",
    expectedLabel: 'LIKELY_GENUINE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Genuine',
  },

  // ──────────────────────────────────────────────
  //  FAKE — 5 examples
  // ──────────────────────────────────────────────
  {
    id: 'fake-01',
    category: 'Sensational Headline',
    headline: 'Shocking! Scientists Reveal The Universe Could Delete Itself At Any Moment!',
    text: 'The end of everything is nearing us all! Scientists are reportedly warning that the universe could suddenly disappear at any moment. The mysterious nature of the universe has left researchers questioning what could happen next.',
    expectedLabel: 'LIKELY_FAKE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Fake',
  },
  {
    id: 'fake-02',
    category: 'Highly Emotional Political',
    headline: "UNREAL! OBAMA TAKES SHOT AT TRUMP With Approving Nod From Germany's Merkel",
    text: 'Obama took a veiled shot at President Trump that was described as beyond tacky. The article uses strongly emotional language to describe a political interaction and suggests that the former president was deliberately trolling Trump.',
    expectedLabel: 'LIKELY_FAKE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Fake',
  },
  {
    id: 'fake-03',
    category: 'Political Commentary',
    headline: 'Why Trump Won; Why Clinton Lost',
    text: 'The article discusses the 2016 presidential election and presents an argumentative explanation of why Donald Trump won and Hillary Clinton lost. It uses political commentary and interpretation rather than a straightforward news-reporting style.',
    expectedLabel: 'LIKELY_FAKE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Fake',
  },
  {
    id: 'fake-04',
    category: 'Highly Sensational Political Story',
    headline: 'Trump Just Literally Gave The WWE A Cabinet Position; World Doomed',
    text: "The article discusses Donald Trump's nomination of Linda McMahon, a former WWE executive, to a government position. The headline uses exaggerated language to frame the appointment as catastrophic.",
    expectedLabel: 'LIKELY_FAKE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Fake',
  },
  {
    id: 'fake-05',
    category: 'Political Commentary',
    headline: "Right Wing Fear Profiteers Warn Of Coming 'Civil War' Over Scalia's 'Murder'",
    text: 'The article presents strongly opinionated political commentary about reactions following the death of Supreme Court Justice Antonin Scalia and discusses claims about a possible political conflict.',
    expectedLabel: 'LIKELY_FAKE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Expected Fake',
  },

  // ──────────────────────────────────────────────
  //  AMBIGUOUS — 4 examples
  // ──────────────────────────────────────────────
  {
    id: 'ambiguous-01',
    category: 'Technology',
    headline: 'Researchers announce new findings from artificial intelligence study',
    text: 'Researchers have reported new findings from a study examining the use of artificial intelligence in several applications. The researchers said additional testing is needed before the results can be applied more broadly. Experts have expressed different views about the possible implications of the findings.',
    expectedBehavior: 'LOWER_CONFIDENCE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Lower Confidence',
  },
  {
    id: 'ambiguous-02',
    category: 'Economy',
    headline: 'Economists discuss possible changes in the global economy',
    text: 'A group of economists has discussed recent changes in economic conditions and their possible effects on businesses and consumers. Some analysts expect conditions to improve, while others believe uncertainty could continue. Further economic data will be needed before a clear long-term trend can be established.',
    expectedBehavior: 'LOWER_CONFIDENCE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Lower Confidence',
  },
  {
    id: 'ambiguous-03',
    category: 'Health Research',
    headline: 'New study examines possible effects of changing lifestyles',
    text: 'Researchers have published a study examining the possible relationship between changing lifestyles and several health outcomes. The researchers said the results provide useful information but emphasized that additional studies are needed to determine whether the observed relationship represents a direct cause.',
    expectedBehavior: 'LOWER_CONFIDENCE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Lower Confidence',
  },
  {
    id: 'ambiguous-04',
    category: 'Climate',
    headline: 'Researchers study changes in regional climate conditions',
    text: 'Scientists are studying changes observed in climate conditions across several regions. The researchers said the available data show some notable differences compared with previous observations, although more research is required to determine the factors responsible for the changes.',
    expectedBehavior: 'LOWER_CONFIDENCE',
    sourceType: 'demo-test',
    sourceLabel: 'DEMO TEST — Lower Confidence',
  },
];
