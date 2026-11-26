-- =============================================================================
-- AI Scheme Sahayak: Seed Data
-- Verified Government & State Schemes + Model CSR Records
-- =============================================================================

USE ai_scheme_sahayak;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE checklist_items;
TRUNCATE TABLE application_checklists;
TRUNCATE TABLE saved_schemes;
TRUNCATE TABLE match_result;
TRUNCATE TABLE guide_step;
TRUNCATE TABLE scheme_document;
TRUNCATE TABLE eligibility_rule;
TRUNCATE TABLE scheme_verification_history;
TRUNCATE TABLE scheme_master;
TRUNCATE TABLE audit_logs;
TRUNCATE TABLE admin_users;
SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------------------------------------------
-- 1. SCHEME MASTER DATA
-- -----------------------------------------------------------------------------
INSERT INTO scheme_master (
    id, scheme_code, scheme_name, scheme_name_hi,
    scheme_description, scheme_description_hi,
    scheme_category, authority_level, ministry_or_org,
    eligible_states, target_beneficiary_groups,
    benefit_type, max_benefit_amount, subsidy_percentage, subsidy_info,
    application_deadline, deadline_note, official_url, source_url,
    scheme_status, verification_status, last_verified_date
) VALUES
(
    1, 'PMEGP',
    'Prime Minister''s Employment Generation Programme (PMEGP)',
    'प्रधानमंत्री रोजगार सृजन कार्यक्रम (PMEGP)',
    'Credit-linked capital subsidy programme for generating self-employment micro-enterprises in manufacturing and services.',
    'विनिर्माण और सेवा क्षेत्र में नए सूक्ष्म उद्यमों के लिए क्रेडिट-लिंक्ड पूंजी सब्सिडी योजना।',
    'Credit-Linked Capital Subsidy', 'Central', 'Ministry of MSME / KVIC',
    'All India', 'New Entrepreneurs, SC/ST, OBC, Women, Minorities, PwD, Rural/Urban',
    'Capital Subsidy + Bank Loan', 5000000.00, 35.00, '15% to 35% margin money capital subsidy credited by KVIC',
    NULL, 'Ongoing / Continuous rolling applications', 'https://www.kviconline.gov.in/pmegpeportal/', 'https://msme.gov.in',
    'Active', 'Verified', '2026-10-15'
),
(
    2, 'STANDUP-INDIA',
    'Stand-Up India Scheme',
    'स्टैंड-अप इंडिया योजना',
    'Facilitates bank loans between Rs 10 Lakh and Rs 1 Crore to at least one SC or ST borrower and at least one Woman borrower per bank branch for greenfield enterprises.',
    'अनुसूचित जाति (SC), अनुसूचित जनजाति (ST) और महिला उद्यमियों को नए व्यवसाय के लिए 10 लाख से 1 करोड़ रुपये तक का बैंक ऋण।',
    'Greenfield Composite Loan', 'Central', 'Ministry of Finance / SIDBI',
    'All India', 'SC, ST, and Women Entrepreneurs (Greenfield First-Time Ventures)',
    'Term Loan + Working Capital', 10000000.00, 0.00, 'Up to 85% composite project loan; borrower contribution min 10-15%',
    NULL, 'Ongoing / Central bank branches nationwide', 'https://www.standupmitra.in', 'https://www.myscheme.gov.in',
    'Active', 'Verified', '2026-10-20'
),
(
    3, 'PMMY-MUDRA',
    'Pradhan Mantri MUDRA Yojana (PMMY)',
    'प्रधानमंत्री मुद्रा योजना (PMMY)',
    'Provides collateral-free institutional credit up to Rs 20 Lakh to non-corporate, non-farm micro and small enterprises across manufacturing, trading, and services.',
    'गैर-कृषि सूक्ष्म एवं लघु व्यवसायों को बिना गारंटी 20 लाख रुपये तक का संस्थागत ऋण (शिशु, किशोर, तरुण, तरुण प्लस)।',
    'Collateral-Free Micro Credit', 'Central', 'MUDRA Ltd / Department of Financial Services',
    'All India', 'Micro & Small Business Founders, Women, Marginalized Traders, Artisans',
    'Collateral-Free Term & Working Capital Loan', 2000000.00, 0.00, 'Shishu (up to 50k), Kishore (50k-5L), Tarun (5L-10L), Tarun Plus (10L-20L)',
    NULL, 'Ongoing / Available at all commercial banks & MFIs', 'https://www.mudra.org.in', 'https://www.jansamarth.in',
    'Active', 'Verified', '2026-11-01'
),
(
    4, 'PM-VISHWAKARMA',
    'PM Vishwakarma Scheme',
    'पीएम विश्वकर्मा योजना',
    'Comprehensive ecosystem support for traditional artisans and craftspersons across 18 family-based trades: skill training, Rs 15,000 toolkit incentive, and collateral-free loans at 5% interest.',
    'पारंपरिक 18 व्यवसायों के कारीगरों को कौशल प्रशिक्षण, 15,000 रुपये का टूलकिट और 5% रियायती ब्याज पर बिना गारंटी ऋण।',
    'Artisan Skill & Credit Ecosystem', 'Central', 'Ministry of MSME',
    'All India', 'Traditional Artisans & Craftspersons (Blacksmith, Carpenter, Tailor, Potter, Cobbler, etc.)',
    'Collateral-Free Loan + Toolkit Grant + Stipend', 300000.00, 0.00, '1st Tranche up to Rs 1 Lakh; 2nd Tranche up to Rs 2 Lakh at 5% interest with GOI subvention',
    NULL, 'Ongoing / Apply via Common Service Centres (CSC)', 'https://pmvishwakarma.gov.in', 'https://msme.gov.in',
    'Active', 'Verified', '2026-10-18'
),
(
    5, 'NSSH',
    'National SC-ST Hub (NSSH)',
    'राष्ट्रीय अनुसूचित जाति-जनजाति हब (NSSH)',
    'Empowers SC/ST entrepreneurs to participate in public procurement processes, offering subsidy on technology adoption, certification reimbursement, and handholding.',
    'अनुसूचित जाति और अनुसूचित जनजाति के उद्यमियों को सार्वजनिक खरीद, तकनीकी उन्नयन और प्रमाणन प्रतिपूर्ति में सहायता।',
    'Market Linkage & Capacity Building', 'Central', 'Ministry of MSME / NSIC',
    'All India', 'SC and ST Micro & Small Entrepreneurs',
    'Reimbursement Subsidies & Tender Handholding', 500000.00, 80.00, 'Up to 80% subsidy for trade fairs, ZED/ISO certification, and tech bank adoption',
    NULL, 'Ongoing / Continuous enterprise registration', 'https://www.scsthub.in', 'https://msme.gov.in',
    'Active', 'Verified', '2026-09-30'
),
(
    6, 'CGTMSE',
    'Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE)',
    'सूक्ष्म एवं लघु उद्यम क्रेडिट गारंटी योजना (CGTMSE)',
    'Provides credit guarantee cover to lending institutions so MSEs can obtain collateral-free loans without third-party guarantees.',
    'उद्यम पंजीकृत सूक्ष्म एवं लघु उद्योगों को बिना गारंटी बैंक ऋण दिलाने हेतु गारंटी कवर।',
    'Credit Guarantee', 'Central', 'Ministry of MSME & SIDBI',
    'All India', 'Udyam-Registered MSEs, Women Founders, SC/ST MSEs',
    'Credit Guarantee Cover (up to Rs 10 Crore)', 100000000.00, 0.00, 'Up to 90% guarantee coverage for women-owned MSEs; up to 85% for SC/ST and micro units',
    NULL, 'Ongoing / Applied via Member Lending Banks', 'https://www.cgtmse.in', 'https://msme.gov.in',
    'Active', 'Verified', '2026-10-12'
),
(
    7, 'SISFS',
    'Startup India Seed Fund Scheme (SISFS)',
    'स्टार्टअप इंडिया सीड फंड योजना (SISFS)',
    'Provides financial assistance to DPIIT-recognized early-stage startups for proof of concept, prototype development, product trials, and commercialization.',
    'DPIIT-मान्यता प्राप्त शुरुआती स्टार्टअप्स को प्रोटोटाइप और बाज़ार परीक्षण के लिए सीड ग्रांट और ऋण सहायता।',
    'Innovation Seed Funding', 'Central', 'DPIIT, Ministry of Commerce & Industry',
    'All India', 'DPIIT-Recognized Startups (Pvt Ltd, LLP, <= 2 years old)',
    'Grant (up to Rs 20L) & Convertible Debt (up to Rs 50L)', 7000000.00, 0.00, 'Up to Rs 20 Lakh non-dilutive grant + up to Rs 50 Lakh debt through approved incubators',
    NULL, 'Rolling cohort cycles via designated incubators', 'https://seedfund.startupindia.gov.in', 'https://www.startupindia.gov.in',
    'Active', 'Verified', '2026-11-05'
),
(
    8, 'NSFDC-MSY',
    'NSFDC Mahila Samriddhi Yojana (MSY)',
    'एनएसएफडीसी महिला समृद्धि योजना (MSY)',
    'Microfinance loan scheme providing highly subsidized credit to Scheduled Caste women entrepreneurs and Self-Help Groups.',
    'अनुसूचित जाति की महिला उद्यमियों और स्वयं सहायता समूहों के लिए 4% रियायती ब्याज दर पर सूक्ष्म वित्त ऋण।',
    'Concessional Microfinance', 'Central', 'NSFDC, Ministry of Social Justice & Empowerment',
    'All India', 'Scheduled Caste (SC) Women Entrepreneurs (Age 18-55, Family Income <= 3 Lakh)',
    'Microfinance Term Loan', 140000.00, 0.00, 'Concessional 4% per annum interest rate with 3-4 years repayment',
    NULL, 'Ongoing / Apply via State SC Development Corporations or PM-SURAJ', 'https://nsfdc.nic.in', 'https://pmsuraj.dosje.gov.in',
    'Active', 'Verified', '2026-10-25'
),
(
    9, 'PM-SVANIDHI',
    'PM Street Vendor''s AtmaNirbhar Nidhi (PM SVANidhi)',
    'पीएम स्वनिधि (स्ट्रीट वेंडर आत्मनिर्भर निधि)',
    'Micro-credit facility offering working capital loans to urban and peri-urban street vendors with 7% interest subsidy and digital cashbacks.',
    'रेहड़ी-पटरी वालों को 10k/20k/50k तक बिना गारंटी कार्यशील पूंजी ऋण और 7% ब्याज सब्सिडी।',
    'Working Capital Micro-Credit', 'Central', 'Ministry of Housing and Urban Affairs (MoHUA)',
    'All India', 'Urban & Peri-Urban Street Vendors, Hawkers, Small Retail Stalls',
    'Sequential Working Capital Loans', 50000.00, 0.00, 'Tranches of Rs 15,000, Rs 25,000, and Rs 50,000 with 7% interest subsidy',
    NULL, 'Ongoing / Apply via pmsvanidhi.mohua.gov.in', 'https://pmsvanidhi.mohua.gov.in', 'https://www.jansamarth.in',
    'Active', 'Verified', '2026-11-02'
),
(
    10, 'UP-MMYSY',
    'Mukhyamantri Yuva Swarojgar Yojana (UP-MMYSY)',
    'मुख्यमंत्री युवा स्वरोजगार योजना (उत्तर प्रदेश)',
    'State government credit-linked margin money subsidy scheme to encourage educated unemployed youth in Uttar Pradesh to establish industrial or service units.',
    'उत्तर प्रदेश के युवाओं को उद्योग (25 लाख तक) व सेवा (10 लाख तक) इकाई लगाने हेतु 25% तक मार्जिन मनी सब्सिडी।',
    'State Self-Employment Subsidy', 'State', 'Department of MSME and Export Promotion, Uttar Pradesh',
    'Uttar Pradesh', 'Unemployed Youth & Entrepreneurs domiciled in Uttar Pradesh (Age 18-40, Min 10th Pass)',
    'Capital Subsidy + Bank Loan', 2500000.00, 25.00, '25% margin money subsidy (max Rs 6.25L for industry, Rs 2.5L for service)',
    NULL, 'Annual state quotas / Apply via District Industries Centre (DIC)', 'https://diupmsme.upsdc.gov.in', 'https://diupmsme.upsdc.gov.in',
    'Active', 'Verified', '2026-10-10'
),
(
    11, 'UP-ODOP-MARGIN',
    'UP One District One Product (ODOP) Margin Money Scheme',
    'एक जनपद एक उत्पाद (ODOP) मार्जिन मनी योजना (उत्तर प्रदेश)',
    'Targeted financial assistance and margin money subsidy for entrepreneurs in Uttar Pradesh setting up or modernizing units aligned with their district''s designated craft/product.',
    'उत्तर प्रदेश के चिन्हित विशिष्ट जिला उत्पादों (शिल्प, वस्त्र, खाद्य, इत्र आदि) के लिए 10% से 25% मार्जिन मनी अनुदान।',
    'State Targeted Craft & Sector Subsidy', 'State', 'Directorate of Industries, Government of Uttar Pradesh',
    'Uttar Pradesh', 'Entrepreneurs in Uttar Pradesh engaged in designated ODOP products/trades',
    'Margin Money Subsidy + Bank Term Loan', 2000000.00, 25.00, 'Subsidy: 25% up to 25L project, 20% up to 50L, 10% above 50L (capped at 20L max)',
    NULL, 'Ongoing / Apply through UP DIC portal', 'https://diupmsme.upsdc.gov.in', 'https://odopup.in',
    'Active', 'Verified', '2026-10-14'
),
(
    12, 'DEMO-CSR-VENTURE',
    '[Demo Record] Inclusive Livelihoods Private CSR Micro-Venture Accelerator',
    '[डेमो रिकॉर्ड] समावेशी आजीविका निजी सीएसआर सूक्ष्म-उद्यम त्वरक',
    'Illustrative corporate social responsibility (CSR) non-dilutive seed grant, mentorship, and equipment acceleration for marginalized founders.',
    'महिला, दिव्यांग और वंचित वर्ग के उद्यमियों के लिए निजी कॉर्पोरेट सीएसआर अनुदान व मेंटरशिप (डेमो रिकॉर्ड)।',
    'Private CSR Seed Accelerator', 'CSR', 'Inclusive Livelihoods CSR Foundation (Demonstration Model)',
    'All India', 'Women, SC, ST, Transgender, and Differently-Abled Early-Stage Founders',
    'Non-Dilutive Seed Grant + 6-Month Mentorship', 500000.00, 100.00, '100% Grant up to Rs 5 Lakh + business coaching and digital bookkeeping',
    '2027-03-31', 'Demo Record / Next cohort application target: March 2027', 'https://www.startupindia.gov.in', 'https://www.startupindia.gov.in',
    'Active', 'Demo', '2026-11-01'
);

-- -----------------------------------------------------------------------------
-- 2. ELIGIBILITY RULES
-- -----------------------------------------------------------------------------
INSERT INTO eligibility_rule (
    scheme_id, min_age, max_age,
    eligible_genders, gender_mandatory,
    eligible_categories, category_mandatory,
    eligible_states, state_mandatory,
    max_household_income, income_mandatory,
    eligible_sectors, sector_mandatory,
    eligible_stages, stage_mandatory,
    min_funding, max_funding, funding_mandatory,
    location_preference, requires_udyam, keywords, special_criteria,
    weight_category, weight_gender, weight_state, weight_income, weight_sector, weight_stage, weight_funding
) VALUES
(1, 18, NULL, 'All', FALSE, 'All', FALSE, 'All India', FALSE, NULL, FALSE,
 'Manufacturing,Services,Food Processing,Handicrafts,Textiles,Agri-Allied,Repair & Maintenance,Technology', TRUE,
 'Startup,Ideation', TRUE, 50000.00, 5000000.00, TRUE,
 'All', FALSE, 'pmegp,subsidy,margin money,manufacturing,service,workshop,unit',
 'New enterprises only. Service sector project cost max Rs 20L; Manufacturing max Rs 50L. Higher 25%-35% subsidy for SC/ST/OBC/Women/Minorities/Rural.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(2, 18, NULL, 'Female,Male,Transgender,Other', TRUE, 'SC,ST,General,OBC,Minority,EWS', TRUE, 'All India', FALSE, NULL, FALSE,
 'Manufacturing,Services,Trading,Agri-Allied,Food Processing,Handicrafts,Textiles,Technology', TRUE,
 'Startup,Ideation', TRUE, 1000000.00, 10000000.00, TRUE,
 'All', FALSE, 'standup,greenfield,sc,st,women,10 lakh,1 crore,factory',
 'Mandatory condition: Applicant must be EITHER SC/ST (any gender) OR a Woman (any category) setting up a first-time greenfield venture needing Rs 10L-1Cr.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(3, 18, NULL, 'All', FALSE, 'All', FALSE, 'All India', FALSE, NULL, FALSE,
 'Manufacturing,Trading,Services,Food Processing,Handicrafts,Textiles,Agri-Allied,Retail,Repair & Maintenance,Technology', FALSE,
 'Ideation,Startup,Existing MSME', FALSE, 10000.00, 2000000.00, TRUE,
 'All', FALSE, 'mudra,loan,collateral free,shishu,kishore,tarun,working capital,shop,retail',
 'Non-farm micro enterprise. Tarun Plus (10L-20L) reserved for past borrowers who repaid standard Tarun loans.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(4, 18, NULL, 'All', FALSE, 'All', FALSE, 'All India', FALSE, NULL, FALSE,
 'Handicrafts,Textiles,Repair & Maintenance,Services,Manufacturing', TRUE,
 'Startup,Existing MSME', FALSE, 10000.00, 300000.00, TRUE,
 'All', FALSE, 'vishwakarma,artisan,craft,carpenter,potter,tailor,blacksmith,cobbler,barber,toolkit,5 percent',
 'Traditional artisan working with hands and tools in one of 18 notified trades. Beneficiary must not have active default under similar credit schemes.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(5, 18, NULL, 'All', FALSE, 'SC,ST', TRUE, 'All India', FALSE, NULL, FALSE,
 'All', FALSE, 'Startup,Existing MSME', FALSE, 25000.00, 500000.00, FALSE,
 'All', TRUE, 'scsthub,nsic,tender,procurement,exhibition,zed,iso,technology adoption',
 'Strictly for SC and ST entrepreneurs with valid Udyam registration aiming to supply to CPSUs and government procurement.',
 25.00, 10.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(6, 18, NULL, 'All', FALSE, 'All', FALSE, 'All India', FALSE, NULL, FALSE,
 'Manufacturing,Services,Trading,Food Processing,Handicrafts,Textiles,Technology', TRUE,
 'Startup,Existing MSME', FALSE, 100000.00, 100000000.00, TRUE,
 'All', TRUE, 'cgtmse,guarantee,collateral free,udyam,bank loan,expansion',
 'Requires valid Udyam registration. Up to 90% guarantee for women founders and up to 85% for SC/ST and micro units.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(7, 18, NULL, 'All', FALSE, 'All', FALSE, 'All India', FALSE, NULL, FALSE,
 'Technology,Services,Manufacturing,Agri-Allied,Food Processing', TRUE,
 'Ideation,Startup', TRUE, 200000.00, 7000000.00, TRUE,
 'All', FALSE, 'startup,seed fund,dpiit,prototype,grant,convertible debt,tech,innovation',
 'Must be a DPIIT-recognized startup incorporated <= 2 years ago as Pvt Ltd, LLP, or Registered Partnership. At least 51% Indian shareholding.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(8, 18, 55, 'Female', TRUE, 'SC', TRUE, 'All India', FALSE, 300000.00, TRUE,
 'All', FALSE, 'Ideation,Startup,Existing MSME', FALSE, 10000.00, 140000.00, TRUE,
 'All', FALSE, 'nsfdc,mahila,samriddhi,sc women,microfinance,shg,concessional',
 'Mandatory: Scheduled Caste (SC) women aged 18 to 55 with total annual household income <= Rs 3,00,000.',
 25.00, 20.00, 10.00, 15.00, 10.00, 10.00, 10.00),

(9, 18, NULL, 'All', FALSE, 'All', FALSE, 'All India', FALSE, 300000.00, FALSE,
 'Trading,Retail,Food Processing,Services', TRUE,
 'Startup,Existing MSME', FALSE, 5000.00, 50000.00, TRUE,
 'Urban', FALSE, 'svanidhi,street vendor,hawker,thela,vegetable seller,working capital',
 'Must hold a Certificate of Vending or Urban Local Body Letter of Recommendation.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00),

(10, 18, 40, 'All', FALSE, 'All', FALSE, 'Uttar Pradesh', TRUE, NULL, FALSE,
 'Manufacturing,Services,Food Processing,Handicrafts,Textiles,Repair & Maintenance,Technology', TRUE,
 'Startup,Ideation', TRUE, 50000.00, 2500000.00, TRUE,
 'All', FALSE, 'up,yuva,swarojgar,uttar pradesh,dic,subsidy,youth,margin money',
 'Mandatory Uttar Pradesh domicile, age 18-40, and minimum 10th pass educational qualification. Industry max 25L, Service max 10L.',
 20.00, 15.00, 25.00, 10.00, 15.00, 10.00, 5.00),

(11, 18, NULL, 'All', FALSE, 'All', FALSE, 'Uttar Pradesh', TRUE, NULL, FALSE,
 'Handicrafts,Textiles,Food Processing,Manufacturing', TRUE,
 'Startup,Existing MSME,Ideation', FALSE, 50000.00, 2000000.00, TRUE,
 'All', FALSE, 'odop,one district,up,artisan,craft,carpet,brassware,chikankari,leather,pottery',
 'Must be located in Uttar Pradesh and produce/process the specific designated ODOP product of that district.',
 20.00, 15.00, 25.00, 10.00, 15.00, 10.00, 5.00),

(12, 18, NULL, 'Female,Transgender,Other,Male', FALSE, 'SC,ST,OBC,Minority,EWS,Other', TRUE, 'All India', FALSE, 600000.00, FALSE,
 'All', FALSE, 'Ideation,Startup', TRUE, 50000.00, 500000.00, TRUE,
 'All', FALSE, 'csr,grant,seed,inclusive,women,transgender,pwd,coaching',
 'Demo Record: Prioritizes marginalized women, SC/ST, and disabled founders seeking prototype seed support.',
 20.00, 15.00, 15.00, 15.00, 15.00, 10.00, 10.00);

-- -----------------------------------------------------------------------------
-- 3. SCHEME DOCUMENTS
-- -----------------------------------------------------------------------------
INSERT INTO scheme_document (scheme_id, document_name, document_name_hi, description, is_mandatory, document_category, sort_order) VALUES
(1, 'Aadhaar Card & PAN Card', 'आधार कार्ड और पैन कार्ड', 'Identity and address proof of entrepreneur', TRUE, 'Identity & Address', 1),
(1, 'Caste / Special Category Certificate', 'जाति / विशेष श्रेणी प्रमाण पत्र', 'Required to claim 25%-35% Special Category subsidy rate', FALSE, 'Category Proof', 2),
(1, 'Detailed Project Report (DPR)', 'विस्तृत परियोजना रिपोर्ट (DPR)', 'Project cost summary, equipment details, and revenue projections', TRUE, 'Business Financials', 3),
(1, 'Educational Qualification Certificate (8th+)', 'शैक्षणिक योग्यता प्रमाण पत्र', 'Mandatory for manufacturing > 10L or service > 5L', FALSE, 'Education', 4),

(2, 'Aadhaar & PAN Card', 'आधार और पैन कार्ड', 'KYC proof for loan account opening', TRUE, 'Identity & Address', 1),
(2, 'Caste Certificate (for SC/ST)', 'जाति प्रमाण पत्र (SC/ST के लिए)', 'Not required if applying as a Woman entrepreneur', FALSE, 'Category Proof', 2),
(2, 'Greenfield Business Project Report', 'ग्रीनफील्ड प्रोजेक्ट रिपोर्ट', 'Detailed project plan showing first-time venture setup', TRUE, 'Business Financials', 3),
(2, 'Bank Statements (Last 6 Months)', 'बैंक स्टेटमेंट (पिछले 6 महीने)', 'Personal/business non-default banking track record', TRUE, 'Financial History', 4),

(3, 'Aadhaar Card / Voter ID', 'आधार कार्ड / वोटर आईडी', 'Identity proof of proprietor/partners', TRUE, 'Identity & Address', 1),
(3, 'Business Address & Registration Proof', 'व्यवसाय पता एवं पंजीकरण प्रमाण', 'Udyam Registration, trade license, or lease agreement', TRUE, 'Business Registration', 2),
(3, 'Machinery / Asset Quotation', 'मशीनरी / उपकरण कोटेशन', 'Proforma invoice for machinery or assets to be financed', FALSE, 'Business Financials', 3),

(4, 'Aadhaar Card (Linked to Mobile)', 'आधार कार्ड (मोबाइल से लिंक)', 'For biometric e-KYC authentication at Common Service Centre', TRUE, 'Identity & Address', 1),
(4, 'Active Bank Account & IFSC Details', 'सक्रिय बैंक खाता एवं IFSC', 'For DBT toolkit incentive voucher and loan disbursement', TRUE, 'Banking', 2),
(4, 'Ration Card / Family Proof', 'राशन कार्ड / परिवार प्रमाण', 'To verify one-member-per-family eligibility limit', TRUE, 'Family Proof', 3),

(5, 'Udyam Registration Certificate', 'उद्यम पंजीकरण प्रमाण पत्र', 'Must show SC or ST ownership status', TRUE, 'Business Registration', 1),
(5, 'Caste Certificate of Promoters', 'प्रवर्तक जाति प्रमाण पत्र', 'Issued by competent authority proving SC/ST status', TRUE, 'Category Proof', 2),
(5, 'Bank Cancelled Cheque', 'बैंक निरस्त चेक', 'For direct subsidy reimbursement processing', TRUE, 'Banking', 3),

(6, 'Udyam Registration Certificate', 'उद्यम पंजीकरण प्रमाण पत्र', 'Mandatory for all MSEs requesting CGTMSE guarantee cover', TRUE, 'Business Registration', 1),
(6, 'Project Feasibility Report & Financials', 'परियोजना रिपोर्ट व वित्तीय विवरण', 'Cash flows, balance sheets, and collateral-free loan request', TRUE, 'Business Financials', 2),

(7, 'DPIIT Startup Recognition Certificate', 'DPIIT स्टार्टअप मान्यता प्रमाण पत्र', 'Official certificate from Startup India portal', TRUE, 'Recognition', 1),
(7, 'Certificate of Incorporation / LLP Deed', 'निगमन प्रमाण पत्र / एलएलपी डीड', 'Entity must be incorporated <= 2 years ago', TRUE, 'Legal Entity', 2),
(7, 'Product Prototype & Pitch Deck', 'प्रोटोटाइप विवरण व पिच डेक', 'Milestones, prototype readiness, and fund utilization breakdown', TRUE, 'Pitch & Product', 3),

(8, 'Scheduled Caste (SC) Certificate', 'अनुसूचित जाति (SC) प्रमाण पत्र', 'Valid certificate issued by Tehsildar / Competent Authority', TRUE, 'Category Proof', 1),
(8, 'Family Annual Income Certificate', 'पारिवारिक वार्षिक आय प्रमाण पत्र', 'Showing total household income <= Rs 3,00,000 per annum', TRUE, 'Income Proof', 2),
(8, 'Aadhaar Card & Bank Passbook', 'आधार कार्ड एवं बैंक पासबुक', 'Age verification (18-55) and direct account transfer', TRUE, 'Identity & Address', 3),

(9, 'Certificate of Vending / ULB Recommendation', 'वेंडिंग प्रमाण पत्र / नगर निकाय पत्र', 'Issued by Urban Local Body or Town Vending Committee', TRUE, 'Vending ID', 1),
(9, 'Aadhaar-Linked Mobile & Bank Passbook', 'आधार लिंक मोबाइल व बैंक पासबुक', 'For digital cashback setup and DBT loan credit', TRUE, 'Banking', 2),

(10, 'UP Domicile / Niwas Praman Patra', 'उत्तर प्रदेश निवास प्रमाण पत्र', 'Proving permanent residence in Uttar Pradesh', TRUE, 'Domicile', 1),
(10, '10th Class Marksheet / Certificate', '10वीं कक्षा का अंकपत्र / प्रमाण पत्र', 'Minimum educational eligibility proof', TRUE, 'Education', 2),
(10, 'Detailed Project Report (DPR) via DIC', 'विस्तृत प्रोजेक्ट रिपोर्ट (DIC प्रारूप)', 'Cost estimate and bank branch selection in Uttar Pradesh', TRUE, 'Business Financials', 3),

(11, 'UP Domicile & Business Proof in District', 'निवास व जिले में व्यवसाय प्रमाण', 'Proof of operating designated ODOP product in the district', TRUE, 'Domicile & Trade', 1),
(11, 'Artisan Card or Udyam Registration', 'कारीगर कार्ड अथवा उद्यम पंजीकरण', 'Registration confirming engagement in ODOP trade', TRUE, 'Business Registration', 2),
(11, 'Machinery / Raw Material Quotations', 'मशीनरी / सामग्री कोटेशन', 'Vendor quotation for ODOP equipment and modernization', TRUE, 'Business Financials', 3),

(12, 'Founder Identity & Category Self-Declaration', 'संस्थापक पहचान व श्रेणी स्व-घोषणा', 'Proof of marginalized category or woman-led enterprise', TRUE, 'Identity & Address', 1),
(12, '2-Page Social Impact Pitch Note', '2-पृष्ठ का सामाजिक प्रभाव प्रस्ताव', 'Business model, target market, and 6-month milestone budget', TRUE, 'Pitch Note', 2);

-- -----------------------------------------------------------------------------
-- 4. GUIDE STEPS
-- -----------------------------------------------------------------------------
INSERT INTO guide_step (scheme_id, step_number, step_title, step_title_hi, step_description, step_description_hi, tips, official_action_url) VALUES
(1, 1, 'Draft Project Report & Collect Quotations', 'प्रोजेक्ट रिपोर्ट बनाएं और कोटेशन लें', 'Determine capital cost up to 50L (manufacturing) or 20L (service) and gather Aadhaar, caste, and rural certificates.', 'लागत का विवरण तैयार करें और आवश्यक प्रमाण पत्र एकत्र करें।', 'One person per family restriction applies under PMEGP.', 'https://www.kviconline.gov.in/pmegpeportal/'),
(1, 2, 'Submit Online Application on KVIC Portal', 'KVIC पोर्टल पर ऑनलाइन आवेदन करें', 'Fill the online form at kviconline.gov.in, select nodal agency (KVIC/KVIB/DIC) and preferred financing bank.', 'आधिकारिक पोर्टल पर फॉर्म भरें और एजेंसी व बैंक चुनें।', 'Never pay processing fees to unverified middlemen.', 'https://www.kviconline.gov.in/pmegpeportal/'),
(1, 3, 'Complete EDP Training & Receive Subsidy', 'EDP प्रशिक्षण पूरा करें और सब्सिडी पाएं', 'After in-principle bank approval, complete mandatory EDP entrepreneurship training to unlock margin money.', 'बैंक स्वीकृति के बाद अनिवार्य उद्यमिता प्रशिक्षण पूरा करें।', 'Subsidy is held in TDR for 3 years before adjustment.', 'https://www.kviconline.gov.in/pmegpeportal/'),

(2, 1, 'Verify Greenfield & Shareholding Condition', 'ग्रीनफील्ड और हिस्सेदारी की शर्त जांचें', 'Ensure the enterprise is your first venture, and at least 51% ownership is held by SC/ST or Woman founder.', 'सुनिश्चित करें कि यह आपका पहला उद्यम है और कम से कम 51% हिस्सेदारी SC/ST या महिला की है।', 'Both manufacturing, services, and agri-allied are eligible.', 'https://www.standupmitra.in'),
(2, 2, 'Register on Stand-Up Mitra Portal', 'स्टैंड-अप मित्र पोर्टल पर पंजीकरण करें', 'Create your borrower profile on standupmitra.in to connect with District Lead Banks and support agencies.', 'standupmitra.in पर प्रोफ़ाइल बनाएं और बैंक से जुड़ें।', 'Request handholding assistance for DPR preparation if needed.', 'https://www.standupmitra.in'),
(2, 3, 'Bank Sanction & 15% Margin Money', 'बैंक स्वीकृति और 15% मार्जिन मनी', 'Coordinate with the matched bank branch for composite sanction and maintain 10-15% own contribution.', 'बैंक शाखा में दस्तावेज़ जमा कर स्वीकृति प्राप्त करें।', 'Repayment period is up to 7 years with 18 months moratorium.', 'https://www.standupmitra.in'),

(3, 1, 'Choose Mudra Loan Category', 'मुद्रा ऋण श्रेणी चुनें', 'Select Shishu (<=50k), Kishore (50k-5L), Tarun (5L-10L), or Tarun Plus (10L-20L) based on funding need.', 'अपनी आवश्यकता अनुसार शिशु, किशोर या तरुण श्रेणी का चयन करें।', 'No collateral or third-party guarantee is required under PMMY.', 'https://www.mudra.org.in'),
(3, 2, 'Apply via JanSamarth or Nearest Bank Branch', 'जनसमर्थ पोर्टल या बैंक शाखा से आवेदन करें', 'Submit application on jansamarth.in or visit any Public, Private, RRB or Small Finance Bank.', 'jansamarth.in पर ऑनलाइन या बैंक में ऑफलाइन फॉर्म भरें।', 'Obtain free Udyam registration first to speed up processing.', 'https://www.jansamarth.in'),

(4, 1, 'Biometric Registration via Common Service Centre', 'जन सेवा केंद्र (CSC) से बायोमेट्रिक पंजीकरण', 'Visit your nearest CSC with Aadhaar, linked mobile phone, bank passbook, and ration card.', 'CSC केंद्र पर आधार बायोमेट्रिक प्रमाणीकरण के साथ पंजीकरण कराएं।', 'Registration is completely free of charge on pmvishwakarma.gov.in.', 'https://pmvishwakarma.gov.in'),
(4, 2, 'Panchayat & District Verification', 'ग्राम पंचायत व जिला स्तरीय सत्यापन', 'Wait for 3-tier verification from Gram Panchayat/ULB, District Implementation Committee, and Screening.', 'ग्राम पंचायत और जिला समिति द्वारा सत्यापन का इंतजार करें।', 'Receive SMS notification on your registered mobile number.', 'https://pmvishwakarma.gov.in'),
(4, 3, '5-7 Days Basic Training & 1st Loan Tranche', 'कौशल प्रशिक्षण व ऋण की पहली किस्त', 'Attend basic skill training with Rs 500/day stipend, receive Rs 15k toolkit e-voucher, and apply for Rs 1L loan.', 'प्रशिक्षण लेकर टूलकिट ई-वाउचर और 5% ब्याज पर 1 लाख तक ऋण लें।', 'Repay in 18 months to unlock 2nd tranche of Rs 2 Lakh.', 'https://pmvishwakarma.gov.in'),

(10, 1, 'Verify UP Domicile & Educational Certificate', 'उत्तर प्रदेश निवास व 10वीं प्रमाण पत्र जांचें', 'Ensure you are a resident of UP aged 18-40 with at least 10th pass qualification.', 'उत्तर प्रदेश निवास और आयु व शैक्षणिक योग्यता की पुष्टि करें।', 'Industry projects can go up to 25L; service projects up to 10L.', 'https://diupmsme.upsdc.gov.in'),
(10, 2, 'Apply via DIUP MSME Portal', 'DIUP MSME पोर्टल पर ऑनलाइन आवेदन करें', 'Register on diupmsme.upsdc.gov.in and select Mukhyamantri Yuva Swarojgar Yojana.', 'पोर्टल पर आवेदन पत्र भरकर जिला उद्योग केंद्र को प्रेषित करें।', 'Track status using your application reference number.', 'https://diupmsme.upsdc.gov.in');

-- -----------------------------------------------------------------------------
-- 5. INITIAL DEFAULT ADMIN USER
-- Password hash for 'Admin@Sahayak2026' generated via Werkzeug PBKDF2-SHA256
-- -----------------------------------------------------------------------------
INSERT INTO admin_users (id, username, email, password_hash, role, is_active) VALUES
(1, 'superadmin', 'admin@schemesahayak.gov.in', 'pbkdf2:sha256:600000$tJ9f8Q2k$9d2757597f805a420b9255ec4dfdbba3783a54d58849b29cb115d9cf7e189814', 'super_admin', TRUE);

INSERT INTO audit_logs (admin_id, action, target_type, target_id, details, ip_address) VALUES
(1, 'DATABASE_SEED', 'SYSTEM', 1, 'Initialized 12 verified schemes, eligibility rules, documents and application steps.', '127.0.0.1');

INSERT INTO scheme_verification_history (scheme_id, verified_by, verification_status, notes)
SELECT id, 1, verification_status, CONCAT('Initial official data audit completed on ', last_verified_date)
FROM scheme_master;
