"""Verified Scheme Knowledge Base with In-Memory / SQLite Fallback and Full MySQL Integration."""
from typing import Any, Dict, List, Optional
from backend.app.database.db import fetch_all, fetch_one, DatabaseConnectionError

# Verified 12 Central, State & Model CSR Schemes with Full Rules, Required Documents and Guidance Steps
VERIFIED_SCHEMES_DATA = [
    {
        "id": 1,
        "scheme_code": "PMEGP",
        "scheme_name": "Prime Minister's Employment Generation Programme (PMEGP)",
        "scheme_name_hi": "प्रधानमंत्री रोजगार सृजन कार्यक्रम (PMEGP)",
        "scheme_description": "Credit-linked capital subsidy programme for generating self-employment micro-enterprises in manufacturing and services.",
        "scheme_description_hi": "विनिर्माण और सेवा क्षेत्र में नए सूक्ष्म उद्यमों के लिए क्रेडिट-लिंक्ड पूंजी सब्सिडी योजना।",
        "scheme_category": "Credit-Linked Capital Subsidy",
        "authority_level": "Central",
        "ministry_or_org": "Ministry of MSME / KVIC",
        "eligible_states": "All India",
        "target_beneficiary_groups": "New Entrepreneurs, SC/ST, OBC, Women, Minorities, PwD, Rural/Urban",
        "benefit_type": "Capital Subsidy + Bank Loan",
        "max_benefit_amount": 5000000.00,
        "subsidy_percentage": 35.00,
        "subsidy_info": "15% to 35% margin money capital subsidy credited by KVIC",
        "application_deadline": None,
        "deadline_note": "Ongoing / Continuous rolling applications",
        "official_url": "https://www.kviconline.gov.in/pmegpeportal/",
        "source_url": "https://msme.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-10-15",
        "is_demo": 0,
        # Eligibility Rules
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Manufacturing,Services,Food Processing,Handicrafts,Textiles,Agri-Allied,Repair & Maintenance,Technology", "sector_mandatory": True,
        "eligible_stages": "Startup,Ideation", "stage_mandatory": True,
        "min_funding": 50000.00, "max_funding": 5000000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "pmegp,subsidy,margin money,manufacturing,service,workshop,unit",
        "special_criteria": "New enterprises only. Service sector max Rs 20L; Manufacturing max Rs 50L. Higher 25%-35% subsidy for SC/ST/OBC/Women/Minorities/Rural.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 1, "document_name": "Aadhaar Card & PAN Card", "document_name_hi": "आधार कार्ड और पैन कार्ड", "description": "Identity and address proof of entrepreneur", "is_mandatory": True, "document_category": "Identity & Address"},
            {"id": 2, "document_name": "Caste / Special Category Certificate", "document_name_hi": "जाति / विशेष श्रेणी प्रमाण पत्र", "description": "Required to claim 25%-35% Special Category subsidy rate", "is_mandatory": False, "document_category": "Category Proof"},
            {"id": 3, "document_name": "Detailed Project Report (DPR)", "document_name_hi": "विस्तृत परियोजना रिपोर्ट (DPR)", "description": "Project cost summary, equipment details, and revenue projections", "is_mandatory": True, "document_category": "Business Financials"},
            {"id": 4, "document_name": "Educational Qualification Certificate (8th+)", "document_name_hi": "शैक्षणिक योग्यता प्रमाण पत्र", "description": "Mandatory for manufacturing > 10L or service > 5L", "is_mandatory": False, "document_category": "Education"}
        ],
        "guide_steps": [
            {"id": 1, "step_number": 1, "step_title": "Online Registration on PMEGP e-Portal", "step_title_hi": "PMEGP ई-पोर्टल पर ऑनलाइन पंजीकरण", "step_description": "Visit kviconline.gov.in/pmegpeportal, fill in Aadhaar KYC and personal/business data.", "official_action_url": "https://www.kviconline.gov.in/pmegpeportal/"},
            {"id": 2, "step_number": 2, "step_title": "Upload DPR and Project Documents", "step_title_hi": "DPR और प्रोजेक्ट दस्तावेज अपलोड करें", "step_description": "Upload detailed project report, caste certificate, and bank branch preference.", "official_action_url": None},
            {"id": 3, "step_number": 3, "step_title": "Task Force Committee Scrutiny & Bank Sanction", "step_title_hi": "टास्क फोर्स जांच और बैंक ऋण स्वीकृति", "step_description": "District Task Force approves application and forwards to selected financing bank branch.", "official_action_url": None},
            {"id": 4, "step_number": 4, "step_title": "EDP Training & Margin Money Credit", "step_title_hi": "EDP प्रशिक्षण और मार्जिन मनी क्रेडिट", "step_description": "Complete mandatory Entrepreneurship Development Programme (EDP) to receive capital subsidy.", "official_action_url": None}
        ]
    },
    {
        "id": 2,
        "scheme_code": "STANDUP-INDIA",
        "scheme_name": "Stand-Up India Scheme",
        "scheme_name_hi": "स्टैंड-अप इंडिया योजना",
        "scheme_description": "Facilitates bank loans between Rs 10 Lakh and Rs 1 Crore to at least one SC or ST borrower and at least one Woman borrower per bank branch for greenfield enterprises.",
        "scheme_description_hi": "अनुसूचित जाति (SC), अनुसूचित जनजाति (ST) और महिला उद्यमियों को नए व्यवसाय के लिए 10 लाख से 1 करोड़ रुपये तक का बैंक ऋण।",
        "scheme_category": "Greenfield Composite Loan",
        "authority_level": "Central",
        "ministry_or_org": "Ministry of Finance / SIDBI",
        "eligible_states": "All India",
        "target_beneficiary_groups": "SC, ST, and Women Entrepreneurs (Greenfield First-Time Ventures)",
        "benefit_type": "Term Loan + Working Capital",
        "max_benefit_amount": 10000000.00,
        "subsidy_percentage": 0.00,
        "subsidy_info": "Up to 85% composite project loan; borrower contribution min 10-15%",
        "application_deadline": None,
        "deadline_note": "Ongoing / Central bank branches nationwide",
        "official_url": "https://www.standupmitra.in",
        "source_url": "https://www.myscheme.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-10-20",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "Female,Male,Transgender,Other", "gender_mandatory": True,
        "eligible_categories": "SC,ST,General,OBC,Minority,EWS", "category_mandatory": True,
        "eligible_sectors": "Manufacturing,Services,Trading,Agri-Allied,Food Processing,Handicrafts,Textiles,Technology", "sector_mandatory": True,
        "eligible_stages": "Startup,Ideation", "stage_mandatory": True,
        "min_funding": 1000000.00, "max_funding": 10000000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "standup,greenfield,sc,st,women,10 lakh,1 crore,factory",
        "special_criteria": "Mandatory condition: Applicant must be EITHER SC/ST (any gender) OR a Woman (any category) setting up a first-time greenfield venture needing Rs 10L-1Cr.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 5, "document_name": "Aadhaar & PAN Card", "document_name_hi": "आधार और पैन कार्ड", "description": "KYC proof for loan account opening", "is_mandatory": True, "document_category": "Identity & Address"},
            {"id": 6, "document_name": "Caste Certificate (for SC/ST)", "document_name_hi": "जाति प्रमाण पत्र (SC/ST के लिए)", "description": "Not required if applying as a Woman entrepreneur", "is_mandatory": False, "document_category": "Category Proof"},
            {"id": 7, "document_name": "Greenfield Business Project Report", "document_name_hi": "ग्रीनफील्ड प्रोजेक्ट रिपोर्ट", "description": "Detailed project plan showing first-time venture setup", "is_mandatory": True, "document_category": "Business Financials"},
            {"id": 8, "document_name": "Bank Statements (Last 6 Months)", "document_name_hi": "बैंक स्टेटमेंट (पिछले 6 महीने)", "description": "Personal/business non-default banking track record", "is_mandatory": True, "document_category": "Financial History"}
        ],
        "guide_steps": [
            {"id": 5, "step_number": 1, "step_title": "Register on Stand-Up Mitra Portal", "step_title_hi": "Stand-Up Mitra पोर्टल पर रजिस्टर करें", "step_description": "Visit standupmitra.in and fill borrower profile as Woman or SC/ST applicant.", "official_action_url": "https://www.standupmitra.in"},
            {"id": 6, "step_number": 2, "step_title": "Handholding Support Selection", "step_title_hi": "हैंडहोल्डिंग सहायता चयन", "step_description": "Connect with Lead District Manager or SIDBI handholding agencies for DPR finalization.", "official_action_url": None},
            {"id": 7, "step_number": 3, "step_title": "Bank Branch Application & Sanction", "step_title_hi": "बैंक आवेदन एवं स्वीकृति", "step_description": "Lending bank evaluates greenfield viability and releases composite loan tranches.", "official_action_url": None}
        ]
    },
    {
        "id": 3,
        "scheme_code": "PMMY-MUDRA",
        "scheme_name": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "scheme_name_hi": "प्रधानमंत्री मुद्रा योजना (PMMY)",
        "scheme_description": "Provides collateral-free institutional credit up to Rs 20 Lakh to non-corporate, non-farm micro and small enterprises across manufacturing, trading, and services.",
        "scheme_description_hi": "गैर-कृषि सूक्ष्म एवं लघु व्यवसायों को बिना गारंटी 20 लाख रुपये तक का संस्थागत ऋण (शिशु, किशोर, तरुण, तरुण प्लस)।",
        "scheme_category": "Collateral-Free Micro Credit",
        "authority_level": "Central",
        "ministry_or_org": "MUDRA Ltd / Department of Financial Services",
        "eligible_states": "All India",
        "target_beneficiary_groups": "Micro & Small Business Founders, Women, Marginalized Traders, Artisans",
        "benefit_type": "Collateral-Free Term & Working Capital Loan",
        "max_benefit_amount": 2000000.00,
        "subsidy_percentage": 0.00,
        "subsidy_info": "Shishu (up to 50k), Kishore (50k-5L), Tarun (5L-10L), Tarun Plus (10L-20L)",
        "application_deadline": None,
        "deadline_note": "Ongoing / Available at all commercial banks & MFIs",
        "official_url": "https://www.mudra.org.in",
        "source_url": "https://www.jansamarth.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-11-01",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Manufacturing,Trading,Services,Food Processing,Handicrafts,Textiles,Agri-Allied,Retail,Repair & Maintenance,Technology", "sector_mandatory": False,
        "eligible_stages": "Ideation,Startup,Existing MSME", "stage_mandatory": False,
        "min_funding": 10000.00, "max_funding": 2000000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "mudra,loan,collateral free,shishu,kishore,tarun,working capital,shop,retail",
        "special_criteria": "Non-farm micro enterprise. Tarun Plus (10L-20L) reserved for past borrowers who repaid standard Tarun loans.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 9, "document_name": "Aadhaar Card / Voter ID", "document_name_hi": "आधार कार्ड / वोटर आईडी", "description": "Identity proof of proprietor/partners", "is_mandatory": True, "document_category": "Identity & Address"},
            {"id": 10, "document_name": "Business Address & Registration Proof", "document_name_hi": "व्यवसाय पता एवं पंजीकरण प्रमाण", "description": "Udyam Registration, trade license, or lease agreement", "is_mandatory": True, "document_category": "Business Registration"},
            {"id": 11, "document_name": "Machinery / Asset Quotation", "document_name_hi": "मशीनरी / उपकरण कोटेशन", "description": "Proforma invoice for machinery or assets to be financed", "is_mandatory": False, "document_category": "Business Financials"}
        ],
        "guide_steps": [
            {"id": 8, "step_number": 1, "step_title": "Choose Loan Category (Shishu, Kishore, Tarun)", "step_title_hi": "ऋण श्रेणी चुनें (शिशु, किशोर, तरुण)", "step_description": "Determine capital requirement: Shishu (<50k), Kishore (50k-5L), Tarun (5L-10L).", "official_action_url": "https://www.jansamarth.in"},
            {"id": 9, "step_number": 2, "step_title": "Apply Online via JanSamarth or Bank Branch", "step_title_hi": "JanSamarth पोर्टल या बैंक शाखा पर आवेदन", "step_description": "Submit application with business plan and asset quotations.", "official_action_url": "https://www.jansamarth.in"}
        ]
    },
    {
        "id": 4,
        "scheme_code": "PM-VISHWAKARMA",
        "scheme_name": "PM Vishwakarma Scheme",
        "scheme_name_hi": "पीएम विश्वकर्मा योजना",
        "scheme_description": "Comprehensive ecosystem support for traditional artisans and craftspersons across 18 family-based trades: skill training, Rs 15,000 toolkit incentive, and collateral-free loans at 5% interest.",
        "scheme_description_hi": "पारंपरिक 18 व्यवसायों के कारीगरों को कौशल प्रशिक्षण, 15,000 रुपये का टूलकिट और 5% रियायती ब्याज पर बिना गारंटी ऋण।",
        "scheme_category": "Artisan Skill & Credit Ecosystem",
        "authority_level": "Central",
        "ministry_or_org": "Ministry of MSME",
        "eligible_states": "All India",
        "target_beneficiary_groups": "Traditional Artisans & Craftspersons (Blacksmith, Carpenter, Tailor, Potter, Cobbler, etc.)",
        "benefit_type": "Collateral-Free Loan + Toolkit Grant + Stipend",
        "max_benefit_amount": 300000.00,
        "subsidy_percentage": 0.00,
        "subsidy_info": "1st Tranche up to Rs 1 Lakh; 2nd Tranche up to Rs 2 Lakh at 5% interest with GOI subvention",
        "application_deadline": None,
        "deadline_note": "Ongoing / Apply via Common Service Centres (CSC)",
        "official_url": "https://pmvishwakarma.gov.in",
        "source_url": "https://msme.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-10-18",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Handicrafts,Textiles,Repair & Maintenance,Services,Manufacturing", "sector_mandatory": True,
        "eligible_stages": "Startup,Existing MSME", "stage_mandatory": False,
        "min_funding": 10000.00, "max_funding": 300000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "vishwakarma,artisan,craft,carpenter,potter,tailor,blacksmith,cobbler,barber,toolkit,5 percent",
        "special_criteria": "Traditional artisan working with hands and tools in one of 18 notified trades. Beneficiary must not have active default under similar credit schemes.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 12, "document_name": "Aadhaar Card (Linked to Mobile)", "document_name_hi": "आधार कार्ड (मोबाइल से लिंक)", "description": "For biometric e-KYC authentication at Common Service Centre", "is_mandatory": True, "document_category": "Identity & Address"},
            {"id": 13, "document_name": "Active Bank Account & IFSC Details", "document_name_hi": "सक्रिय बैंक खाता एवं IFSC", "description": "For DBT toolkit incentive voucher and loan disbursement", "is_mandatory": True, "document_category": "Banking"}
        ],
        "guide_steps": [
            {"id": 10, "step_number": 1, "step_title": "Biometric CSC Registration", "step_title_hi": "CSC केंद्र पर बायोमेट्रिक पंजीकरण", "step_description": "Visit nearest Common Service Centre (CSC) with Aadhaar and mobile for biometric verification.", "official_action_url": "https://pmvishwakarma.gov.in"},
            {"id": 11, "step_number": 2, "step_title": "Gram Panchayat / ULB Verification", "step_title_hi": "ग्राम पंचायत / नगर निकाय सत्यापन", "step_description": "Local committee verifies family trade practices.", "official_action_url": None},
            {"id": 12, "step_number": 3, "step_title": "5-7 Days Basic Skill Training", "step_title_hi": "5-7 दिवसीय बुनियादी कौशल प्रशिक्षण", "step_description": "Receive Rs 500/day stipend during training and Rs 15,000 e-voucher for modern tools.", "official_action_url": None}
        ]
    },
    {
        "id": 5,
        "scheme_code": "NSSH",
        "scheme_name": "National SC-ST Hub (NSSH)",
        "scheme_name_hi": "राष्ट्रीय अनुसूचित जाति-जनजाति हब (NSSH)",
        "scheme_description": "Empowers SC/ST entrepreneurs to participate in public procurement processes, offering subsidy on technology adoption, certification reimbursement, and handholding.",
        "scheme_description_hi": "अनुसूचित जाति और अनुसूचित जनजाति के उद्यमियों को सार्वजनिक खरीद, तकनीकी उन्नयन और प्रमाणन प्रतिपूर्ति में सहायता।",
        "scheme_category": "Market Linkage & Capacity Building",
        "authority_level": "Central",
        "ministry_or_org": "Ministry of MSME / NSIC",
        "eligible_states": "All India",
        "target_beneficiary_groups": "SC and ST Micro & Small Entrepreneurs",
        "benefit_type": "Reimbursement Subsidies & Tender Handholding",
        "max_benefit_amount": 500000.00,
        "subsidy_percentage": 80.00,
        "subsidy_info": "Up to 80% subsidy for trade fairs, ZED/ISO certification, and tech bank adoption",
        "application_deadline": None,
        "deadline_note": "Ongoing / Continuous enterprise registration",
        "official_url": "https://www.scsthub.in",
        "source_url": "https://msme.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-09-30",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "SC,ST", "category_mandatory": True,
        "eligible_sectors": "All", "sector_mandatory": False,
        "eligible_stages": "Startup,Existing MSME", "stage_mandatory": False,
        "min_funding": 25000.00, "max_funding": 500000.00, "funding_mandatory": False,
        "location_preference": "All", "requires_udyam": True,
        "keywords": "scsthub,nsic,tender,procurement,exhibition,zed,iso,technology adoption",
        "special_criteria": "Strictly for SC and ST entrepreneurs with valid Udyam registration aiming to supply to CPSUs and government procurement.",
        "weight_category": 25.00, "weight_gender": 10.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 14, "document_name": "Udyam Registration Certificate", "document_name_hi": "उद्यम पंजीकरण प्रमाण पत्र", "description": "Must show SC or ST ownership status", "is_mandatory": True, "document_category": "Business Registration"},
            {"id": 15, "document_name": "Caste Certificate of Promoters", "document_name_hi": "प्रवर्तक जाति प्रमाण पत्र", "description": "Issued by competent authority proving SC/ST status", "is_mandatory": True, "document_category": "Category Proof"}
        ],
        "guide_steps": [
            {"id": 13, "step_number": 1, "step_title": "Register with Udyam & SC/ST Hub Portal", "step_title_hi": "उद्यम एवं SC/ST हब पोर्टल पर पंजीकरण", "step_description": "Verify your enterprise as SC/ST majority-owned on scsthub.in.", "official_action_url": "https://www.scsthub.in"}
        ]
    },
    {
        "id": 6,
        "scheme_code": "CGTMSE",
        "scheme_name": "Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE)",
        "scheme_name_hi": "सूक्ष्म एवं लघु उद्यम क्रेडिट गारंटी योजना (CGTMSE)",
        "scheme_description": "Provides credit guarantee cover to lending institutions so MSEs can obtain collateral-free loans without third-party guarantees.",
        "scheme_description_hi": "उद्यम पंजीकृत सूक्ष्म एवं लघु उद्योगों को बिना गारंटी बैंक ऋण दिलाने हेतु गारंटी कवर।",
        "scheme_category": "Credit Guarantee",
        "authority_level": "Central",
        "ministry_or_org": "Ministry of MSME & SIDBI",
        "eligible_states": "All India",
        "target_beneficiary_groups": "Udyam-Registered MSEs, Women Founders, SC/ST MSEs",
        "benefit_type": "Credit Guarantee Cover (up to Rs 10 Crore)",
        "max_benefit_amount": 100000000.00,
        "subsidy_percentage": 0.00,
        "subsidy_info": "Up to 90% guarantee coverage for women-owned MSEs; up to 85% for SC/ST and micro units",
        "application_deadline": None,
        "deadline_note": "Ongoing / Applied via Member Lending Banks",
        "official_url": "https://www.cgtmse.in",
        "source_url": "https://msme.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-10-12",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Manufacturing,Services,Trading,Food Processing,Handicrafts,Textiles,Technology", "sector_mandatory": True,
        "eligible_stages": "Startup,Existing MSME", "stage_mandatory": False,
        "min_funding": 100000.00, "max_funding": 100000000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": True,
        "keywords": "cgtmse,guarantee,collateral free,udyam,bank loan,expansion",
        "special_criteria": "Requires valid Udyam registration. Up to 90% guarantee for women founders and up to 85% for SC/ST and micro units.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 16, "document_name": "Udyam Registration Certificate", "document_name_hi": "उद्यम पंजीकरण प्रमाण पत्र", "description": "Mandatory for all MSEs requesting CGTMSE guarantee cover", "is_mandatory": True, "document_category": "Business Registration"},
            {"id": 17, "document_name": "Project Feasibility Report & Financials", "document_name_hi": "परियोजना रिपोर्ट व वित्तीय विवरण", "description": "Cash flows, balance sheets, and collateral-free loan request", "is_mandatory": True, "document_category": "Business Financials"}
        ],
        "guide_steps": [
            {"id": 14, "step_number": 1, "step_title": "Approach Member Lending Institution", "step_title_hi": "सदस्य बैंक शाखा में आवेदन", "step_description": "Apply for collateral-free MSME loan under CGTMSE cover at any scheduled commercial bank.", "official_action_url": "https://www.cgtmse.in"}
        ]
    },
    {
        "id": 7,
        "scheme_code": "SISFS",
        "scheme_name": "Startup India Seed Fund Scheme (SISFS)",
        "scheme_name_hi": "स्टार्टअप इंडिया सीड फंड योजना (SISFS)",
        "scheme_description": "Provides financial assistance to DPIIT-recognized early-stage startups for proof of concept, prototype development, product trials, and commercialization.",
        "scheme_description_hi": "DPIIT-मान्यता प्राप्त शुरुआती स्टार्टअप्स को प्रोटोटाइप और बाज़ार परीक्षण के लिए सीड ग्रांट और ऋण सहायता।",
        "scheme_category": "Innovation Seed Funding",
        "authority_level": "Central",
        "ministry_or_org": "DPIIT, Ministry of Commerce & Industry",
        "eligible_states": "All India",
        "target_beneficiary_groups": "DPIIT-Recognized Startups (Pvt Ltd, LLP, <= 2 years old)",
        "benefit_type": "Grant (up to Rs 20L) & Convertible Debt (up to Rs 50L)",
        "max_benefit_amount": 7000000.00,
        "subsidy_percentage": 0.00,
        "subsidy_info": "Up to Rs 20 Lakh non-dilutive grant + up to Rs 50 Lakh debt through approved incubators",
        "application_deadline": None,
        "deadline_note": "Rolling cohort cycles via designated incubators",
        "official_url": "https://seedfund.startupindia.gov.in",
        "source_url": "https://www.startupindia.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-11-05",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Technology,Services,Manufacturing,Agri-Allied,Food Processing", "sector_mandatory": True,
        "eligible_stages": "Ideation,Startup", "stage_mandatory": True,
        "min_funding": 200000.00, "max_funding": 7000000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "startup,seed fund,dpiit,prototype,grant,convertible debt,tech,innovation",
        "special_criteria": "Must be a DPIIT-recognized startup incorporated <= 2 years ago as Pvt Ltd, LLP, or Registered Partnership. At least 51% Indian shareholding.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 18, "document_name": "DPIIT Startup Recognition Certificate", "document_name_hi": "DPIIT स्टार्टअप मान्यता प्रमाण पत्र", "description": "Official certificate from Startup India portal", "is_mandatory": True, "document_category": "Recognition"},
            {"id": 19, "document_name": "Product Prototype & Pitch Deck", "document_name_hi": "प्रोटोटाइप विवरण व पिच डेक", "description": "Milestones, prototype readiness, and fund utilization breakdown", "is_mandatory": True, "document_category": "Pitch & Product"}
        ],
        "guide_steps": [
            {"id": 15, "step_number": 1, "step_title": "DPIIT Recognition", "step_title_hi": "DPIIT स्टार्टअप मान्यता प्राप्त करें", "step_description": "Register entity on startupindia.gov.in and receive DPIIT certificate.", "official_action_url": "https://seedfund.startupindia.gov.in"}
        ]
    },
    {
        "id": 8,
        "scheme_code": "NSFDC-MSY",
        "scheme_name": "NSFDC Mahila Samriddhi Yojana (MSY)",
        "scheme_name_hi": "एनएसएफडीसी महिला समृद्धि योजना (MSY)",
        "scheme_description": "Microfinance loan scheme providing highly subsidized credit to Scheduled Caste women entrepreneurs and Self-Help Groups.",
        "scheme_description_hi": "अनुसूचित जाति की महिला उद्यमियों और स्वयं सहायता समूहों के लिए 4% रियायती ब्याज दर पर सूक्ष्म वित्त ऋण।",
        "scheme_category": "Concessional Microfinance",
        "authority_level": "Central",
        "ministry_or_org": "NSFDC, Ministry of Social Justice & Empowerment",
        "eligible_states": "All India",
        "target_beneficiary_groups": "Scheduled Caste (SC) Women Entrepreneurs (Age 18-55, Family Income <= 3 Lakh)",
        "benefit_type": "Microfinance Term Loan",
        "max_benefit_amount": 140000.00,
        "subsidy_percentage": 0.00,
        "subsidy_info": "Concessional 4% per annum interest rate with 3-4 years repayment",
        "application_deadline": None,
        "deadline_note": "Ongoing / Apply via State SC Development Corporations or PM-SURAJ",
        "official_url": "https://nsfdc.nic.in",
        "source_url": "https://pmsuraj.dosje.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-10-25",
        "is_demo": 0,
        "min_age": 18, "max_age": 55,
        "eligible_genders": "Female", "gender_mandatory": True,
        "eligible_categories": "SC", "category_mandatory": True,
        "eligible_sectors": "All", "sector_mandatory": False,
        "eligible_stages": "Ideation,Startup,Existing MSME", "stage_mandatory": False,
        "min_funding": 10000.00, "max_funding": 140000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "nsfdc,mahila,samriddhi,sc women,microfinance,shg,concessional",
        "special_criteria": "Mandatory: Scheduled Caste (SC) women aged 18 to 55 with total annual household income <= Rs 3,00,000.",
        "weight_category": 25.00, "weight_gender": 20.00, "weight_state": 10.00, "weight_income": 15.00, "weight_sector": 10.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 20, "document_name": "Scheduled Caste (SC) Certificate", "document_name_hi": "अनुसूचित जाति (SC) प्रमाण पत्र", "description": "Valid certificate issued by Tehsildar / Competent Authority", "is_mandatory": True, "document_category": "Category Proof"},
            {"id": 21, "document_name": "Family Annual Income Certificate", "document_name_hi": "पारिवारिक वार्षिक आय प्रमाण पत्र", "description": "Showing total household income <= Rs 3,00,000 per annum", "is_mandatory": True, "document_category": "Income Proof"}
        ],
        "guide_steps": [
            {"id": 16, "step_number": 1, "step_title": "Apply via State Channelizing Agency or PM-SURAJ", "step_title_hi": "राज्य एजेंसी अथवा PM-SURAJ पोर्टल पर आवेदन", "step_description": "Submit application through State Scheduled Castes Finance & Development Corporation.", "official_action_url": "https://pmsuraj.dosje.gov.in"}
        ]
    },
    {
        "id": 9,
        "scheme_code": "PM-SVANIDHI",
        "scheme_name": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        "scheme_name_hi": "पीएम स्वनिधि (स्ट्रीट वेंडर आत्मनिर्भर निधि)",
        "scheme_description": "Micro-credit facility offering working capital loans to urban and peri-urban street vendors with 7% interest subsidy and digital cashbacks.",
        "scheme_description_hi": "रेहड़ी-पटरी वालों को 10k/20k/50k तक बिना गारंटी कार्यशील पूंजी ऋण और 7% ब्याज सब्सिडी।",
        "scheme_category": "Working Capital Micro-Credit",
        "authority_level": "Central",
        "ministry_or_org": "Ministry of Housing and Urban Affairs (MoHUA)",
        "eligible_states": "All India",
        "target_beneficiary_groups": "Urban & Peri-Urban Street Vendors, Hawkers, Small Retail Stalls",
        "benefit_type": "Sequential Working Capital Loans",
        "max_benefit_amount": 50000.00,
        "subsidy_percentage": 0.00,
        "subsidy_info": "Tranches of Rs 15,000, Rs 25,000, and Rs 50,000 with 7% interest subsidy",
        "application_deadline": None,
        "deadline_note": "Ongoing / Apply via pmsvanidhi.mohua.gov.in",
        "official_url": "https://pmsvanidhi.mohua.gov.in",
        "source_url": "https://www.jansamarth.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-11-02",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Trading,Retail,Food Processing,Services", "sector_mandatory": True,
        "eligible_stages": "Startup,Existing MSME", "stage_mandatory": False,
        "min_funding": 5000.00, "max_funding": 50000.00, "funding_mandatory": True,
        "location_preference": "Urban", "requires_udyam": False,
        "keywords": "svanidhi,street vendor,hawker,thela,vegetable seller,working capital",
        "special_criteria": "Must hold a Certificate of Vending or Urban Local Body Letter of Recommendation.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 22, "document_name": "Certificate of Vending / ULB Recommendation", "document_name_hi": "वेंडिंग प्रमाण पत्र / नगर निकाय पत्र", "description": "Issued by Urban Local Body or Town Vending Committee", "is_mandatory": True, "document_category": "Vending ID"},
            {"id": 23, "document_name": "Aadhaar-Linked Mobile & Bank Passbook", "document_name_hi": "आधार लिंक मोबाइल व बैंक पासबुक", "description": "For digital cashback setup and DBT loan credit", "is_mandatory": True, "document_category": "Banking"}
        ],
        "guide_steps": [
            {"id": 17, "step_number": 1, "step_title": "Online Portal / CSC Vending e-KYC", "step_title_hi": "ऑनलाइन पोर्टल / CSC वेंडिंग e-KYC", "step_description": "Check vending survey status on pmsvanidhi.mohua.gov.in and apply directly.", "official_action_url": "https://pmsvanidhi.mohua.gov.in"}
        ]
    },
    {
        "id": 10,
        "scheme_code": "UP-MMYSY",
        "scheme_name": "Mukhyamantri Yuva Swarojgar Yojana (UP-MMYSY)",
        "scheme_name_hi": "मुख्यमंत्री युवा स्वरोजगार योजना (उत्तर प्रदेश)",
        "scheme_description": "State government credit-linked margin money subsidy scheme to encourage educated unemployed youth in Uttar Pradesh to establish industrial or service units.",
        "scheme_description_hi": "उत्तर प्रदेश के युवाओं को उद्योग (25 लाख तक) व सेवा (10 लाख तक) इकाई लगाने हेतु 25% तक मार्जिन मनी सब्सिडी।",
        "scheme_category": "State Self-Employment Subsidy",
        "authority_level": "State",
        "ministry_or_org": "Department of MSME and Export Promotion, Uttar Pradesh",
        "eligible_states": "Uttar Pradesh",
        "target_beneficiary_groups": "Unemployed Youth & Entrepreneurs domiciled in Uttar Pradesh (Age 18-40, Min 10th Pass)",
        "benefit_type": "Capital Subsidy + Bank Loan",
        "max_benefit_amount": 2500000.00,
        "subsidy_percentage": 25.00,
        "subsidy_info": "25% margin money subsidy (max Rs 6.25L for industry, Rs 2.5L for service)",
        "application_deadline": None,
        "deadline_note": "Annual state quotas / Apply via District Industries Centre (DIC)",
        "official_url": "https://diupmsme.upsdc.gov.in",
        "source_url": "https://diupmsme.upsdc.gov.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-10-10",
        "is_demo": 0,
        "min_age": 18, "max_age": 40,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Manufacturing,Services,Food Processing,Handicrafts,Textiles,Repair & Maintenance,Technology", "sector_mandatory": True,
        "eligible_stages": "Startup,Ideation", "stage_mandatory": True,
        "min_funding": 50000.00, "max_funding": 2500000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "up,yuva,swarojgar,uttar pradesh,dic,subsidy,youth,margin money",
        "special_criteria": "Mandatory Uttar Pradesh domicile, age 18-40, and minimum 10th pass educational qualification. Industry max 25L, Service max 10L.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 25.00, "weight_income": 10.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 5.00,
        "documents": [
            {"id": 24, "document_name": "UP Domicile / Niwas Praman Patra", "document_name_hi": "उत्तर प्रदेश निवास प्रमाण पत्र", "description": "Proving permanent residence in Uttar Pradesh", "is_mandatory": True, "document_category": "Domicile"},
            {"id": 25, "document_name": "10th Class Marksheet / Certificate", "document_name_hi": "10वीं कक्षा का अंकपत्र / प्रमाण पत्र", "description": "Minimum educational eligibility proof", "is_mandatory": True, "document_category": "Education"}
        ],
        "guide_steps": [
            {"id": 18, "step_number": 1, "step_title": "Apply on DIUP MSME Portal", "step_title_hi": "DIUP MSME पोर्टल पर ऑनलाइन आवेदन", "step_description": "Submit online form on diupmsme.upsdc.gov.in selecting your district DIC.", "official_action_url": "https://diupmsme.upsdc.gov.in"}
        ]
    },
    {
        "id": 11,
        "scheme_code": "UP-ODOP-MARGIN",
        "scheme_name": "UP One District One Product (ODOP) Margin Money Scheme",
        "scheme_name_hi": "एक जनपद एक उत्पाद (ODOP) मार्जिन मनी योजना (उत्तर प्रदेश)",
        "scheme_description": "Targeted financial assistance and margin money subsidy for entrepreneurs in Uttar Pradesh setting up or modernizing units aligned with their district's designated craft/product.",
        "scheme_description_hi": "उत्तर प्रदेश के चिन्हित विशिष्ट जिला उत्पादों (शिल्प, वस्त्र, खाद्य, इत्र आदि) के लिए 10% से 25% मार्जिन मनी अनुदान।",
        "scheme_category": "State Targeted Craft & Sector Subsidy",
        "authority_level": "State",
        "ministry_or_org": "Directorate of Industries, Government of Uttar Pradesh",
        "eligible_states": "Uttar Pradesh",
        "target_beneficiary_groups": "Entrepreneurs in Uttar Pradesh engaged in designated ODOP products/trades",
        "benefit_type": "Margin Money Subsidy + Bank Term Loan",
        "max_benefit_amount": 2000000.00,
        "subsidy_percentage": 25.00,
        "subsidy_info": "Subsidy: 25% up to 25L project, 20% up to 50L, 10% above 50L (capped at 20L max)",
        "application_deadline": None,
        "deadline_note": "Ongoing / Apply through UP DIC portal",
        "official_url": "https://diupmsme.upsdc.gov.in",
        "source_url": "https://odopup.in",
        "scheme_status": "Active",
        "verification_status": "Verified",
        "last_verified_date": "2026-10-14",
        "is_demo": 0,
        "min_age": 18, "max_age": None,
        "eligible_genders": "All", "gender_mandatory": False,
        "eligible_categories": "All", "category_mandatory": False,
        "eligible_sectors": "Handicrafts,Textiles,Food Processing,Manufacturing", "sector_mandatory": True,
        "eligible_stages": "Startup,Existing MSME,Ideation", "stage_mandatory": False,
        "min_funding": 50000.00, "max_funding": 2000000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "odop,one district,up,artisan,craft,carpet,brassware,chikankari,leather,pottery",
        "special_criteria": "Must be located in Uttar Pradesh and produce/process the specific designated ODOP product of that district.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 25.00, "weight_income": 10.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 5.00,
        "documents": [
            {"id": 26, "document_name": "UP Domicile & Business Proof in District", "document_name_hi": "निवास व जिले में व्यवसाय प्रमाण", "description": "Proof of operating designated ODOP product in the district", "is_mandatory": True, "document_category": "Domicile & Trade"},
            {"id": 27, "document_name": "Artisan Card or Udyam Registration", "document_name_hi": "कारीगर कार्ड अथवा उद्यम पंजीकरण", "description": "Registration confirming engagement in ODOP trade", "is_mandatory": True, "document_category": "Business Registration"}
        ],
        "guide_steps": [
            {"id": 19, "step_number": 1, "step_title": "Select District ODOP Trade & Apply Online", "step_title_hi": "जिला ODOP उत्पाद चुनें और ऑनलाइन आवेदन करें", "step_description": "Apply through UP DIC portal selecting your district's notified ODOP industry.", "official_action_url": "https://diupmsme.upsdc.gov.in"}
        ]
    },
    {
        "id": 12,
        "scheme_code": "DEMO-CSR-VENTURE",
        "scheme_name": "[Demo Record] Inclusive Livelihoods Private CSR Micro-Venture Accelerator",
        "scheme_name_hi": "[डेमो रिकॉर्ड] समावेशी आजीविका निजी सीएसआर सूक्ष्म-उद्यम त्वरक",
        "scheme_description": "Illustrative corporate social responsibility (CSR) non-dilutive seed grant, mentorship, and equipment acceleration for marginalized founders.",
        "scheme_description_hi": "महिला, दिव्यांग और वंचित वर्ग के उद्यमियों के लिए निजी कॉर्पोरेट सीएसआर अनुदान व मेंटरशिप (डेमो रिकॉर्ड)।",
        "scheme_category": "Private CSR Seed Accelerator",
        "authority_level": "Private_CSR",
        "ministry_or_org": "Inclusive Livelihoods CSR Foundation (Demonstration Model)",
        "eligible_states": "All India",
        "target_beneficiary_groups": "Women, SC, ST, Transgender, and Differently-Abled Early-Stage Founders",
        "benefit_type": "Non-Dilutive Seed Grant + 6-Month Mentorship",
        "max_benefit_amount": 500000.00,
        "subsidy_percentage": 100.00,
        "subsidy_info": "100% Grant up to Rs 5 Lakh + business coaching and digital bookkeeping",
        "application_deadline": "2027-03-31",
        "deadline_note": "Demo Record / Next cohort application target: March 2027",
        "official_url": "https://www.startupindia.gov.in",
        "source_url": "https://www.startupindia.gov.in",
        "scheme_status": "Active",
        "verification_status": "Demo",
        "last_verified_date": "2026-11-01",
        "is_demo": 1,
        "min_age": 18, "max_age": None,
        "eligible_genders": "Female,Transgender,Other,Male", "gender_mandatory": False,
        "eligible_categories": "SC,ST,OBC,Minority,EWS,Other", "category_mandatory": True,
        "eligible_sectors": "All", "sector_mandatory": False,
        "eligible_stages": "Ideation,Startup", "stage_mandatory": True,
        "min_funding": 50000.00, "max_funding": 500000.00, "funding_mandatory": True,
        "location_preference": "All", "requires_udyam": False,
        "keywords": "csr,grant,seed,inclusive,women,transgender,pwd,coaching",
        "special_criteria": "Demo Record: Prioritizes marginalized women, SC/ST, and disabled founders seeking prototype seed support.",
        "weight_category": 20.00, "weight_gender": 15.00, "weight_state": 15.00, "weight_income": 15.00, "weight_sector": 15.00, "weight_stage": 10.00, "weight_funding": 10.00,
        "documents": [
            {"id": 28, "document_name": "Founder Identity Proof", "document_name_hi": "संस्थापक पहचान प्रमाण", "description": "Aadhaar Card, Voter Card or Passport", "is_mandatory": True, "document_category": "Identity & Address"}
        ],
        "guide_steps": [
            {"id": 20, "step_number": 1, "step_title": "Submit Pitch Presentation (Demo)", "step_title_hi": "पिच प्रेजेंटेशन जमा करें (डेमो)", "step_description": "Submit prototype plan for CSR jury evaluation.", "official_action_url": "https://www.startupindia.gov.in"}
        ]
    }
]


def get_all_schemes(active_only: bool = True) -> List[Dict[str, Any]]:
    """Retrieve schemes joined with eligibility rules from MySQL with seamless fallback to verified knowledge base."""
    try:
        query = """
            SELECT sm.*,
                   er.min_age, er.max_age, er.eligible_genders, er.gender_mandatory,
                   er.eligible_categories, er.category_mandatory,
                   er.eligible_states, er.state_mandatory,
                   er.max_household_income, er.income_mandatory,
                   er.eligible_sectors, er.sector_mandatory,
                   er.eligible_stages, er.stage_mandatory,
                   er.min_funding, er.max_funding, er.funding_mandatory,
                   er.location_preference, er.requires_udyam, er.keywords, er.special_criteria,
                   er.weight_category, er.weight_gender, er.weight_state, er.weight_income,
                   er.weight_sector, er.weight_stage, er.weight_funding, er.weight_location, er.weight_support
            FROM scheme_master sm
            LEFT JOIN eligibility_rule er ON er.scheme_id = sm.id
        """
        if active_only:
            query += " WHERE sm.scheme_status = 'Active'"
        query += " ORDER BY sm.authority_level ASC, sm.id ASC"
        rows = fetch_all(query)
        if rows:
            return rows
    except Exception:
        pass

    # Seamless fallback: return verified repository
    if active_only:
        return [s for s in VERIFIED_SCHEMES_DATA if s.get("scheme_status") == "Active"]
    return list(VERIFIED_SCHEMES_DATA)


def get_scheme_by_id(scheme_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve full scheme record with documents and guide steps from MySQL or fallback repository."""
    try:
        scheme = fetch_one(
            """
            SELECT sm.*,
                   er.min_age, er.max_age, er.eligible_genders, er.gender_mandatory,
                   er.eligible_categories, er.category_mandatory,
                   er.eligible_states, er.state_mandatory,
                   er.max_household_income, er.income_mandatory,
                   er.eligible_sectors, er.sector_mandatory,
                   er.eligible_stages, er.stage_mandatory,
                   er.min_funding, er.max_funding, er.funding_mandatory,
                   er.location_preference, er.requires_udyam, er.keywords, er.special_criteria
            FROM scheme_master sm
            LEFT JOIN eligibility_rule er ON er.scheme_id = sm.id
            WHERE sm.id = %s
            """,
            (scheme_id,)
        )
        if scheme:
            scheme["documents"] = fetch_all(
                "SELECT id, document_name, document_name_hi, description, is_mandatory, document_category, sort_order FROM scheme_document WHERE scheme_id = %s ORDER BY sort_order ASC, id ASC",
                (scheme_id,)
            )
            scheme["guide_steps"] = fetch_all(
                "SELECT id, step_number, step_title, step_title_hi, step_description, step_description_hi, tips, official_action_url FROM guide_step WHERE scheme_id = %s ORDER BY step_number ASC",
                (scheme_id,)
            )
            return scheme
    except Exception:
        pass

    # Seamless fallback lookup by ID
    for s in VERIFIED_SCHEMES_DATA:
        if s["id"] == int(scheme_id):
            return dict(s)
    return None


def get_scheme_categories() -> List[str]:
    """Distinct scheme categories."""
    try:
        rows = fetch_all("SELECT DISTINCT scheme_category FROM scheme_master WHERE scheme_status = 'Active' ORDER BY scheme_category")
        if rows:
            return [r["scheme_category"] for r in rows if r.get("scheme_category")]
    except Exception:
        pass

    cats = sorted(list({s["scheme_category"] for s in VERIFIED_SCHEMES_DATA if s.get("scheme_category")}))
    return cats
