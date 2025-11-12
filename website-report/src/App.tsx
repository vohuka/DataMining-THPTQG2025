import React from "react";
import { Card, CardContent } from "./components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./components/ui/tabs";
import { Button } from "./components/ui/button";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  CartesianGrid,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  LabelList,
} from "recharts";
import { motion } from "framer-motion";
import {
  TrendingUp,
  BrainCircuit,
  Sigma,
  Sparkles,
  Building2,
  School,
  ArrowUp,
  Book,
} from "lucide-react";

// --- Data (extracted from the user's PDF report) ---
// Urban Advantage: HCMC mean minus National mean (points)
const urbanAdvantage = [
  { subject: "Toán", diff: 0.48 },
  { subject: "Sinh học", diff: 0.51 },
  { subject: "Tiếng Anh", diff: 0.29 },
  { subject: "Lịch sử", diff: 0.15 },
  { subject: "Địa lí", diff: 0.19 },
  { subject: "GDCD/KTPL", diff: 0.28 },
  { subject: "Ngữ văn", diff: 0.06 },
  { subject: "Vật lí", diff: -0.01 },
  { subject: "Hóa học", diff: -0.11 },
];

// Model performance
const models = [
  { model: "Linear Regression", R2: 0.8946, RMSE: 1.3902 },
  { model: "Random Forest", R2: 0.9582, RMSE: 0.875 },
  { model: "Gradient Boosting", R2: 0.9453, RMSE: 1.0017 },
];

// Age groups (Total score means)
const ageGroups = [
  { group: "18 tuổi", mean: 25.33 },
  { group: "&gt; 18 tuổi", mean: 22.62 },
  { group: "Thi lại", mean: 19.32 },
];

// Study lean (Cohen's d groups)
const leanGroups = [
  { group: "Thiên Toán", mean: 28.78 },
  { group: "Cân bằng", mean: 27.69 },
  { group: "Thiên Văn", mean: 24.57 },
];

// Key metrics
const kpis = [
  {
    icon: <TrendingUp className="w-5 h-5" />,
    label: "R² (Random Forest)",
    value: "0.9582",
  },
  { icon: <Sigma className="w-5 h-5" />, label: "RMSE (RF)", value: "0.875" },
  {
    icon: <Building2 className="w-5 h-5" />,
    label: "Urban advantage (Toán)",
    value: "+0.48",
  },
  {
    icon: <School className="w-5 h-5" />,
    label: "% Toán > 5 (HCM)",
    value: "43.08%",
  },
];

// Correlation snapshot (selected pairs, Pearson r)
const corr = [
  { pair: "Hóa–Sinh", r: 0.75 },
  { pair: "Vật lí–Hóa", r: 0.74 },
  { pair: "Toán–Hóa", r: 0.74 },
  { pair: "Toán–Sinh", r: 0.73 },
  { pair: "Toán–Vật lí", r: 0.69 },
  { pair: "Sử–Địa", r: 0.71 },
  { pair: "Sử–GDCD", r: 0.56 },
  { pair: "Địa–GDCD", r: 0.51 },
  { pair: "Văn–Lý", r: 0.22 },
];

// --- Subject-level stats (HCM vs National) from the PDF (Table: Thống kê mô tả) ---
const subjectStats = [
  {
    subject: "Toán",
    hcm_mean: 5.26,
    nat_mean: 4.78,
    under5_hcm: 43.077,
    under5_nat: 56.395,
    ge7_hcm: 15.028,
    ge7_nat: 12.231,
  },
  {
    subject: "Ngữ văn",
    hcm_mean: 7.06,
    nat_mean: 7.0,
    under5_hcm: 2.85,
    under5_nat: 6.24,
    ge7_hcm: 62.863,
    ge7_nat: 59.572,
  },
  {
    subject: "Tiếng Anh",
    hcm_mean: 5.67,
    nat_mean: 5.38,
    under5_hcm: 30.36,
    under5_nat: 38.22,
    ge7_hcm: 20.034,
    ge7_nat: 15.135,
  },
  {
    subject: "Vật lí",
    hcm_mean: 6.98,
    nat_mean: 6.99,
    under5_hcm: 8.297,
    under5_nat: 9.79,
    ge7_hcm: 52.938,
    ge7_nat: 53.663,
  },
  {
    subject: "Hóa học",
    hcm_mean: 5.95,
    nat_mean: 6.06,
    under5_hcm: 31.731,
    under5_nat: 29.529,
    ge7_hcm: 31.22,
    ge7_nat: 33.667,
  },
  {
    subject: "Sinh học",
    hcm_mean: 6.29,
    nat_mean: 5.78,
    under5_hcm: 20.281,
    under5_nat: 32.44,
    ge7_hcm: 35.793,
    ge7_nat: 25.151,
  },
  {
    subject: "Lịch sử",
    hcm_mean: 6.67,
    nat_mean: 6.52,
    under5_hcm: 13.939,
    under5_nat: 18.63,
    ge7_hcm: 47.64,
    ge7_nat: 43.778,
  },
  {
    subject: "Địa lí",
    hcm_mean: 6.82,
    nat_mean: 6.63,
    under5_hcm: 12.863,
    under5_nat: 18.69,
    ge7_hcm: 49.497,
    ge7_nat: 45.269,
  },
  {
    subject: "GDCD/KTPL",
    hcm_mean: 7.97,
    nat_mean: 7.69,
    under5_hcm: 1.001,
    under5_nat: 2.567,
    ge7_hcm: 86.337,
    ge7_nat: 78.171,
  },
];

// --- Top 5 combinations by mean (and a few lowest), and top 5 by count (from PDF tables) ---
const comboTopMean = [
  { combo: "D66", mean3: 20.95, std: 2.35, n: 8709 },
  { combo: "C20", mean3: 20.77, std: 2.83, n: 6048 },
  { combo: "C19", mean3: 20.41, std: 3.0, n: 3890 },
  { combo: "D11", mean3: 20.19, std: 2.71, n: 31164 },
  { combo: "D14", mean3: 20.19, std: 2.77, n: 7528 },
];
const comboLowMean = [
  { combo: "C12", mean3: 16.21, std: 2.57, n: 251 },
  { combo: "A02", mean3: 15.62, std: 3.37, n: 512 },
  { combo: "B02", mean3: 14.81, std: 3.14, n: 151 },
  { combo: "A05", mean3: 14.47, std: 3.2, n: 224 },
  { combo: "A06", mean3: 13.56, std: 3.24, n: 432 },
];
const comboTopCount = [
  { combo: "D01", mean3: 18.59, n: 62318 },
  { combo: "C01", mean3: 19.96, n: 56975 },
  { combo: "C02", mean3: 18.83, n: 35364 },
  { combo: "C04", mean3: 17.92, n: 34140 },
  { combo: "C03", mean3: 17.76, n: 32136 },
];

// --- RAE & Zodiac Data (NEW) ---
const quarterData = [
  { group: "Q1", total_mean: 25.07, total_std: 4.3, count: 28590 },
  { group: "Q2", total_mean: 24.99, total_std: 4.27, count: 28880 },
  { group: "Q3", total_mean: 25.03, total_std: 4.3, count: 31146 },
  { group: "Q4", total_mean: 25.04, total_std: 4.27, count: 40532 },
];

const zodiacData = [
  { group: "Ma Kết", total_mean: 25.1, total_std: 4.27, count: 10553 },
  { group: "Song Ngư", total_mean: 25.07, total_std: 4.32, count: 9276 },
  { group: "Bảo Bình", total_mean: 25.05, total_std: 4.28, count: 9135 },
  { group: "Xử Nữ", total_mean: 25.05, total_std: 4.29, count: 11017 },
  { group: "Bạch Dương", total_mean: 25.04, total_std: 4.25, count: 9633 },
  { group: "Sư Tử", total_mean: 25.04, total_std: 4.32, count: 10049 },
  { group: "Thiên Bình", total_mean: 25.03, total_std: 4.24, count: 12166 },
  { group: "Nhân Mã", total_mean: 25.03, total_std: 4.29, count: 13625 },
  { group: "Song Tử", total_mean: 25.02, total_std: 4.29, count: 9701 },
  { group: "Bọ Cạp", total_mean: 25.02, total_std: 4.31, count: 13960 },
  { group: "Kim Ngưu", total_mean: 25.01, total_std: 4.27, count: 9873 },
  { group: "Cự Giải", total_mean: 24.97, total_std: 4.29, count: 10160 },
];

type HeatCellProps = { r: number };

const HeatCell: React.FC<HeatCellProps> = ({ r }) => {
  // Map r in [-1,1] to 0..1 and then to light->dark
  const intensity = Math.round(((r + 1) / 2) * 255);
  const bg = `rgb(255, ${255 - intensity}, ${255 - intensity})`; // red-ish scale
  return (
    <div
      className="text-xs font-medium p-2 rounded-md"
      style={{ backgroundColor: bg }}
    >
      {r.toFixed(2)}
    </div>
  );
};

type SectionProps = {
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  children?: React.ReactNode;
};

const Section: React.FC<SectionProps> = ({ title, subtitle, children }) => (
  <section className="space-y-4">
    <div>
      <h2 className="text-xl font-semibold tracking-tight">{title}</h2>
      {subtitle && (
        <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>
      )}
    </div>
    <div className="grid gap-4 lg:grid-cols-12">{children}</div>
  </section>
);

export default function ReportViz() {
  // Responsive hint: make Charts re-calc on resize (avoids zero-width on mobile tab switches)
 React.useEffect(() => {
   if (tabsListRef.current) {
     tabsListRef.current.scrollLeft = 0; // chỉ scroll về đầu khi mount
   }
 }, []);
  // Extra tests
  React.useEffect(() => {
    const labels = [
      ...ageGroups.map((g) => g.group),
      ...leanGroups.map((g) => g.group),
      ...urbanAdvantage.map((s) => s.subject),
      ...kpis.map((k) => k.label),
    ].join(" | ");
    console.assert(
      !/[<>]/.test(labels),
      "Test failed: any display label containing raw < or > must be escaped"
    );
    console.assert(
      urbanAdvantage.length === 9,
      "Test failed: urbanAdvantage must have 9 subjects as per report"
    );
    console.assert(
      subjectStats.length === 9,
      "Test failed: subjectStats must cover 9 subjects"
    );
    console.assert(
      models.length === 3,
      "Test failed: exactly 3 models should be compared"
    );
    console.assert(
      comboTopMean.length === 5 && comboTopCount.length === 5,
      "Test failed: combos top lists should have 5 entries"
    );
    console.assert(kpis.length >= 4, "Test failed: at least 4 KPI cards");
  }, []);
  // Thêm ref cho TabsList để thao tác scroll
  const tabsListRef = React.useRef<HTMLDivElement>(null);

  // Logic để scroll về bên trái khi mount hoặc resize
  React.useEffect(() => {
    const scrollToStart = () => {
      // Thêm delay nhỏ để đảm bảo DOM đã update
      setTimeout(() => {
        if (tabsListRef.current) {
          tabsListRef.current.scrollLeft = 0; // Scroll về vị trí 0 (bên trái)
        }
      }, 0);
    };

    // Scroll ngay khi mount
    scrollToStart();

    // Scroll khi resize (đảm bảo responsive)
    const handleResize = () => scrollToStart();
    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="min-h-screen w-full bg-white">
      <div className="mx-auto px-3 md:px-10 py-8">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-3xl md:text-3xl font-bold justify-center flex">
            THPT 2025 — TP.HCM Data Report (Interactive)
          </h1>
          <p className="text-sm md:text-base text-muted-foreground mt-2 justify-center flex">
            Trực quan hoá những phát hiện chính: lợi thế đô thị, nhóm tuổi, xu
            hướng học (Cohen’s d), hiệu năng mô hình và tương quan môn học.
          </p>
        </motion.div>

        {/* KPI Row */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
          {kpis.map((k, i) => (
            <Card key={i} className="rounded-2xl shadow-sm">
              <CardContent className="p-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {k.icon}
                  <span className="text-xs text-muted-foreground">
                    {k.label}
                  </span>
                </div>
                <div className="text-lg font-semibold">{k.value}</div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Tabs defaultValue="overview" className="mt-8">
          <TabsList
            ref={tabsListRef}
            className="flex gap-2 overflow-x-auto whitespace-nowrap overflow-y-hidden pb-1 pl-0 custom-scrollbar justify-start xl:justify-center"
          >
            {/* Spacer để đảm bảo tab đầu tiên không bị che */}
            <div className="w-2 flex-shrink-0" />

            <TabsTrigger value="overview" className="shrink-0">
              Tổng quan
            </TabsTrigger>
            <TabsTrigger value="subjects" className="shrink-0">
              Theo môn
            </TabsTrigger>
            <TabsTrigger value="urban" className="shrink-0">
              Lợi thế đô thị
            </TabsTrigger>
            <TabsTrigger value="age" className="shrink-0">
              Nhóm tuổi
            </TabsTrigger>
            <TabsTrigger value="lean" className="shrink-0">
              Cohen's d
            </TabsTrigger>
            <TabsTrigger value="combos" className="shrink-0">
              Tổ hợp 3 môn
            </TabsTrigger>
            <TabsTrigger value="models" className="shrink-0">
              Mô hình dự báo
            </TabsTrigger>
            <TabsTrigger value="corr" className="shrink-0">
              Tương quan môn
            </TabsTrigger>
            <TabsTrigger value="rae" className="shrink-0">
              RAE & Cung hoàng đạo
            </TabsTrigger>
            <TabsTrigger value="appendix" className="shrink-0">
              Phụ lục & Tải liệu
            </TabsTrigger>

            {/* Spacer phải để tránh tab cuối bị che */}
            <div className="w-2 flex-shrink-0" />
          </TabsList>

          {/* Overview */}
          <TabsContent value="overview" className="mt-6">
            <Section
              title="Những insight nổi bật"
              subtitle="Trích từ báo cáo gốc; số liệu chính được tái hiện dưới dạng tương tác."
            >
              <div className="lg:col-span-7">
                <Card className="rounded-2xl h-full">
                  <CardContent className="p-6 h-full">
                    <h3 className="font-semibold mb-3 flex items-center gap-2">
                      <BrainCircuit className="w-5 h-5" />
                      Toán là yếu tố quyết định
                    </h3>
                    <ul className="list-disc ml-5 space-y-2 text-sm">
                      <li>
                        SHAP chỉ ra Toán có tác động lớn nhất đến tổng điểm;
                        điểm Toán cao có thể đẩy tổng điểm tăng mạnh, ngược lại
                        điểm thấp kéo giảm mạnh.
                      </li>
                      <li>
                        Nhóm <em>Thiên Toán</em> đạt tổng điểm trung bình cao
                        nhất (≈ 28.78), vượt cả nhóm <em>Cân bằng</em> và{" "}
                        <em>Thiên Văn</em>.
                      </li>
                      <li>
                        <strong>Khuyến nghị:</strong> ưu tiên chiến lược nâng
                        điểm Toán cho nhóm thiên KHXH.
                      </li>
                    </ul>
                    <h3 className="font-semibold mb-3 flex items-center gap-2 mt-4">
                      <Building2 className="w-5 h-5" />
                      Lợi thế đô thị rõ nét ở TPHCM
                    </h3>
                    <ul className="list-disc ml-5 space-y-2 text-sm">
                      <li>
                        Lợi thế đô thị TPHCM ở các môn Toán (+0,48 điểm), Sinh
                        (+0,51 điểm), Tiếng Anh (+0,29 điểm), phản ánh chất
                        lượng giáo dục cao hơn ở các thành phố
                      </li>
                      <li>
                        Tuy nhiên, một phát hiện đáng ngạc nhiên là sự xuất hiện
                        của "bất lợi đô thị" ở hai môn KHTN là Vật lí (-0.01
                        điểm) và Hóa học (-0.11 điểm)
                      </li>
                      <li>
                        <strong>Khuyến nghị:</strong> Cần tìm hiểu nguyên nhân
                        một cách rõ ràng và có biện pháp cải thiện chất lượng
                        giảng dạy hai môn này tại TPHCM.
                      </li>
                    </ul>
                    <h3 className="font-semibold mb-3 flex items-center gap-2 mt-4">
                      <Book className="w-5 h-5" />
                      Xu hướng thí sinh lựa chọn môn và xu hướng học hiện tại
                    </h3>
                    <ul className="list-disc ml-5 space-y-2 text-sm">
                      <li>
                        Xu hướng học tập thiên văn chiếm ưu thế (75,6%), có thể
                        do đề văn dễ hơn hoặc năng lực của học sinh, nhưng không
                        hiệu quả- cần khuyến khích cân bằng hoặc phát triển Toán
                      </li>
                      <li>
                        Thí sinh chọn tổ hợp có Văn (có thể xem là tổ hợp các
                        môn Khoa học xã hội) chiếm đa số như D01 (62318 thí
                        sinh), C01 (56975 thí sinh)
                      </li>
                      <li>
                        Thí sinh chọn tổ hợp có môn GDCD/KTPL lại có điểm số cao
                        nhất
                      </li>
                      <li>
                        <strong>Khuyến nghị:</strong> Cần có chiến lược định
                        hướng chọn môn và tổ hợp phù hợp để tối ưu hoá điểm số
                        và cơ hội trúng tuyển đại học. Cùng với đó, xu hướng học Khoa học xã hội chiếm nhiều hơn so với Khoa học tự nhiên. Thêm vào đó, nếu muốn nâng tổng điểm đáng kể hoặc sẽ phù hợp chọn nếu ai muốn
                        đậu tốt nghiệp THPT nhưng năng lực học không cao hãy chọn môn GDCD/KTPL.
                      </li>
                    </ul>
                    <div className="mt-4 text-xs text-muted-foreground">
                      Nguồn số liệu: PDF gốc, các bảng kết quả & hình minh hoạ.
                    </div>
                  </CardContent>
                </Card>
              </div>
              <div className="lg:col-span-5 grid grid-cols-1 gap-4">
                <Card className="rounded-2xl">
                  <CardContent className="p-4">
                    <div className="text-sm font-medium mb-2">
                      Tổng điểm trung bình theo nhóm xu hướng học
                    </div>
                    <ResponsiveContainer width="100%" height={220}>
                      <BarChart data={leanGroups}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="group" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Bar dataKey="mean">
                          <LabelList
                            dataKey="mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl">
                  <CardContent className="p-4">
                    <div className="text-sm font-medium mb-2">
                      Tổng điểm trung bình theo nhóm tuổi
                    </div>
                    <ResponsiveContainer width="100%" height={220}>
                      <BarChart data={ageGroups}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="group" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Bar dataKey="mean">
                          <LabelList
                            dataKey="mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>

          {/* Urban Advantage */}
          <TabsContent value="urban" className="mt-6">
            <Section
              title="Lợi thế đô thị (TP.HCM so với Toàn quốc)"
              subtitle="Chênh lệch điểm trung bình (điểm)"
            >
              <div className="lg:col-span-12 grid grid-cols-1 xl:grid-cols-3 gap-4">
                <Card className="rounded-2xl xl:col-span-2">
                  <CardContent className="p-6">
                    <ResponsiveContainer width="100%" height={360}>
                      <BarChart
                        data={urbanAdvantage}
                        margin={{ left: 20, right: 20 }}
                      >
                        <CartesianGrid vertical={false} />
                        <XAxis
                          dataKey="subject"
                          tick={{ fontSize: 12 }}
                          interval={0}
                          angle={0}
                          height={40}
                        />
                        <YAxis tick={{ fontSize: 12 }} domain={[-0.5, 0.7]} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="diff" name="HCM - Quốc gia">
                          <LabelList
                            dataKey="diff"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="text-sm text-muted-foreground mt-3">
                      Toán (+0.48) & Sinh (+0.51) nổi bật; Hóa (-0.11) và Vật lí
                      (-0.01) cho thấy "bất lợi" nhẹ.
                    </div>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <div className="text-sm font-medium mb-2">
                      Radar: Chênh lệch theo môn
                    </div>
                    <ResponsiveContainer width="100%" height={320}>
                      <RadarChart data={urbanAdvantage} outerRadius="80%">
                        <PolarGrid />
                        <PolarAngleAxis
                          dataKey="subject"
                          tick={{ fontSize: 10 }}
                        />
                        <PolarRadiusAxis
                          angle={30}
                          domain={[-0.5, 0.7]}
                          tick={{ fontSize: 10 }}
                        />
                        <Radar
                          name="HCM - Quốc gia"
                          dataKey="diff"
                          stroke="#8884d8"
                          fill="#8884d8"
                          fillOpacity={0.5}
                        />
                        <Tooltip />
                      </RadarChart>
                    </ResponsiveContainer>
                    <div className="text-xs text-muted-foreground mt-2">
                      Radar giúp nhìn nhanh môn nào kéo tổng chênh lệch nhiều
                      nhất; vùng âm (Hóa, Lý) dễ nhận ra.
                    </div>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>

          {/* Age groups */}
          <TabsContent value="age" className="mt-6">
            <Section
              title="Nhóm tuổi & phân hoá"
              subtitle="Điểm trung bình tổng cho ba nhóm tuổi"
            >
              <div className="lg:col-span-8">
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <ResponsiveContainer width="100%" height={320}>
                      <BarChart data={ageGroups}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="group" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Bar dataKey="mean">
                          <LabelList
                            dataKey="mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="text-sm text-muted-foreground mt-3">
                      ANOVA cho thấy khác biệt có ý nghĩa giữa các nhóm; nhóm
                      "Thi lại" phân tán mạnh và có trung bình thấp hơn.
                    </div>
                  </CardContent>
                </Card>
              </div>
              <div className="lg:col-span-4 grid gap-4">
                <Card className="rounded-2xl h-full">
                  <CardContent className="p-5">
                    <h3 className="font-semibold mb-2 flex items-center gap-2">
                      <Sparkles className="w-4 h-4" />
                      Gợi ý hành động
                    </h3>
                    <ul className="list-disc ml-5 text-sm space-y-2">
                      <li>
                        Ưu tiên hỗ trợ Toán cho nhóm thiên KHXH & nhóm "Thi
                        lại".
                      </li>
                      <li>
                        Tư vấn chọn tổ hợp theo cụm năng lực (KHTN vs KHXH).
                      </li>
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>

          {/* Leaning (Cohen's d) */}
          <TabsContent value="lean" className="mt-6">
            <Section
              title="Xu hướng học (Cohen’s d)"
              subtitle="So sánh tổng điểm trung bình theo nhóm thiên"
            >
              <div className="lg:col-span-8">
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <ResponsiveContainer width="100%" height={320}>
                      <BarChart data={leanGroups}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="group" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Bar dataKey="mean">
                          <LabelList
                            dataKey="mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="text-sm text-muted-foreground mt-3">
                      Nhóm "Thiên Toán" vượt trội ở hầu hết môn, kể cả Ngữ văn —
                      cho thấy đây là chỉ báo năng lực học tập tổng thể.
                    </div>
                  </CardContent>
                </Card>
              </div>
              <div className="lg:col-span-4">
                <Card className="rounded-2xl h-full">
                  <CardContent className="p-5">
                    <h3 className="font-semibold mb-2">Diễn giải nhanh</h3>
                    <p className="text-sm text-muted-foreground">
                      Cohen’s d dương ⇒ thiên Văn; âm ⇒ thiên Toán. Phân bố d
                      lệch phải mạnh (đa số thiên Văn) nhưng tổng điểm nhóm này
                      lại thấp hơn đáng kể.
                    </p>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>

          {/* Models */}
          <TabsContent value="models" className="mt-6">
            <Section
              title="Mô hình dự báo tổng điểm"
              subtitle="So sánh R² và RMSE (test)"
            >
              <div className="lg:col-span-8">
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <ResponsiveContainer width="100%" height={320}>
                      <BarChart data={models}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="model" tick={{ fontSize: 12 }} />
                        <YAxis
                          yAxisId="left"
                          orientation="left"
                          tick={{ fontSize: 12 }}
                          domain={[0, 1]}
                        />
                        <YAxis
                          yAxisId="right"
                          orientation="right"
                          tick={{ fontSize: 12 }}
                        />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="R2" yAxisId="left" name="R²">
                          <LabelList
                            dataKey="R2"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(3)}
                          />
                        </Bar>
                        <Bar dataKey="RMSE" yAxisId="right" name="RMSE" />
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="text-sm text-muted-foreground mt-3">
                      Random Forest cho hiệu năng tốt nhất (R² ≈ 0.958; RMSE ≈
                      0.875).
                    </div>
                  </CardContent>
                </Card>
              </div>
              <div className="lg:col-span-4">
                <Card className="rounded-2xl h-full">
                  <CardContent className="p-5">
                    <h3 className="font-semibold mb-2">Giải thích mô hình</h3>
                    <p className="text-sm text-muted-foreground">
                      SHAP (trên Gradient Boosting) cho thấy thứ tự quan trọng:
                      Toán ≫ Ngữ văn ≈ Vật lí ≈ Địa lí ≈ Tiếng Anh… Nhóm tuổi
                      "Thi lại" có tác động âm.
                    </p>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>

          {/* Correlation */}
          <TabsContent value="corr" className="mt-6">
            <Section
              title="Tương quan môn học (Pearson r)"
              subtitle="Ảnh màu đỏ đậm thể hiện mức tương quan cao hơn"
            >
              <div className="lg:col-span-7">
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <div className="grid grid-cols-3 gap-3">
                      {corr.map((c, i) => (
                        <div
                          key={i}
                          className="flex items-center justify-between gap-3"
                        >
                          <div className="text-sm font-medium w-28">
                            {c.pair}
                          </div>
                          <HeatCell r={c.r} />
                        </div>
                      ))}
                    </div>
                    <div className="text-sm text-muted-foreground mt-3">
                      KHTN liên kết rất chặt (Toán–Lý–Hoá–Sinh). KHXH cũng kết
                      nối (Sử–Địa–GDCD). Văn & Anh tương đối độc lập.
                    </div>
                  </CardContent>
                </Card>
              </div>
              <div className="lg:col-span-5">
                <Card className="rounded-2xl h-full">
                  <CardContent className="p-5">
                    <h3 className="font-semibold mb-2">
                      Ứng dụng tư vấn tổ hợp
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      Dựa trên cụm tương quan, khuyến nghị chọn tổ hợp theo cụm
                      năng lực để cộng hưởng điểm số và tối đa hoá cơ hội.
                    </p>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>
          {/* Subjects */}
          <TabsContent value="subjects" className="mt-6">
            <Section
              title="Theo môn: HCM vs Toàn quốc"
              subtitle="So sánh Mean và tỷ lệ điểm (％)"
            >
              <div className="lg:col-span-12 grid grid-cols-1 xl:grid-cols-3 gap-4">
                <Card className="rounded-2xl xl:col-span-2">
                  <CardContent className="p-6">
                    <div className="text-sm font-medium mb-2">
                      Mean theo môn
                    </div>
                    <ResponsiveContainer width="100%" height={320}>
                      <BarChart data={subjectStats}>
                        <CartesianGrid vertical={false} />
                        <XAxis
                          dataKey="subject"
                          tick={{ fontSize: 12 }}
                          interval={0}
                          height={40}
                        />
                        <YAxis tick={{ fontSize: 12 }} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="hcm_mean" name="HCM">
                          <LabelList
                            dataKey="hcm_mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                        <Bar dataKey="nat_mean" name="Quốc gia">
                          <LabelList
                            dataKey="nat_mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl">
                  <CardContent className="p-6 space-y-6">
                    <div>
                      <div className="text-sm font-medium mb-2">
                        Tỷ lệ điểm ＜ 5 (％)
                      </div>
                      <ResponsiveContainer width="100%" height={120}>
                        <BarChart data={subjectStats}>
                          <XAxis dataKey="subject" hide />
                          <YAxis hide />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="under5_hcm" name="HCM" />
                          <Bar dataKey="under5_nat" name="Quốc gia" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                    <div>
                      <div className="text-sm font-medium mb-2">
                        Tỷ lệ điểm ≥ 7 (％)
                      </div>
                      <ResponsiveContainer width="100%" height={120}>
                        <BarChart data={subjectStats}>
                          <XAxis dataKey="subject" hide />
                          <YAxis hide />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="ge7_hcm" name="HCM" />
                          <Bar dataKey="ge7_nat" name="Quốc gia" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>

          {/* Combos */}
          <TabsContent value="combos" className="mt-6">
            <Section
              title="Tổ hợp 3 môn"
              subtitle="Top theo điểm trung bình và theo số lượng thí sinh"
            >
              <div className="lg:col-span-12 grid grid-cols-1 xl:grid-cols-3 gap-4">
                <Card className="rounded-2xl xl:col-span-2">
                  <CardContent className="p-6">
                    <div className="text-sm font-medium mb-2">
                      Top 5 theo Mean (3 môn)
                    </div>
                    <ResponsiveContainer width="100%" height={280}>
                      <BarChart data={comboTopMean}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="combo" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="mean3" name="Điểm TB 3 môn">
                          <LabelList
                            dataKey="mean3"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="text-xs text-muted-foreground mt-2">
                      Một số tổ hợp điểm thấp (ví dụ A06 ≈ 13.56) thể hiện độ
                      phân tán lớn và/hoặc độ khó cao.
                    </div>
                  </CardContent>
                </Card>
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <div className="text-sm font-medium mb-2">
                      Top 5 theo Số lượng
                    </div>
                    <ResponsiveContainer width="100%" height={280}>
                      <BarChart data={comboTopCount}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="combo" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="n" name="Số thí sinh">
                          <LabelList dataKey="n" position="top" />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </div>
              <div className="lg:col-span-12 grid grid-cols-1">
                <Card className="rounded-2xl">
                  <CardContent className="p-5">
                    <div className="text-sm font-medium mb-3">
                      Các tổ hợp TB thấp (tham khảo)
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
                      {comboLowMean.map((c, i) => (
                        <div key={i} className="border rounded-xl p-3 text-sm">
                          <div className="font-semibold">{c.combo}</div>
                          <div>TB: {c.mean3.toFixed(2)}</div>
                          <div className="text-xs text-muted-foreground">
                            n={c.n}, sd={c.std.toFixed(2)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>

          {/* RAE & Zodiac -- REPLACED BLOCK */}
          <TabsContent value="rae" className="mt-6">
            <Section
              title="RAE (Relative Age Effect) & Cung hoàng đạo"
              subtitle="So sánh tổng điểm trung bình theo quý sinh và cung hoàng đạo"
            >
              <div className="lg:col-span-12 grid grid-cols-1 xl:grid-cols-2 gap-4">
                {/* Chart 1: Quarters */}
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <h3 className="text-sm font-medium mb-2">
                      Thống kê điểm theo Quý sinh (RAE)
                    </h3>
                    <ResponsiveContainer width="100%" height={320}>
                      <BarChart data={quarterData}>
                        <CartesianGrid vertical={false} />
                        <XAxis dataKey="group" tick={{ fontSize: 12 }} />
                        <YAxis tick={{ fontSize: 12 }} domain={[24.8, 25.2]} />
                        <Tooltip formatter={(v: any) => Number(v).toFixed(2)} />
                        <Bar dataKey="total_mean" name="Tổng điểm TB">
                          <LabelList
                            dataKey="total_mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="text-xs text-muted-foreground mt-2">
                      Ghi chú: Khác biệt về điểm trung bình giữa các quý sinh là
                      rất nhỏ (Q1: 25.07, Q2: 24.99).
                    </div>
                  </CardContent>
                </Card>

                {/* Chart 2: Zodiac */}
                <Card className="rounded-2xl">
                  <CardContent className="p-6">
                    <h3 className="text-sm font-medium mb-2">
                      Thống kê điểm theo Cung Hoàng Đạo
                    </h3>
                    <ResponsiveContainer width="100%" height={320}>
                      <BarChart data={zodiacData} margin={{ bottom: 50 }}>
                        <CartesianGrid vertical={false} />
                        <XAxis
                          dataKey="group"
                          tick={{ fontSize: 11 }}
                          interval={0}
                          angle={-45}
                          textAnchor="end"
                        />
                        <YAxis tick={{ fontSize: 12 }} domain={[24.8, 25.2]} />
                        <Tooltip formatter={(v: any) => Number(v).toFixed(2)} />
                        <Bar dataKey="total_mean" name="Tổng điểm TB">
                          <LabelList
                            dataKey="total_mean"
                            position="top"
                            formatter={(v: any) => Number(v).toFixed(2)}
                            fontSize={10}
                          />
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="text-xs text-muted-foreground mt-2">
                      Ghi chú: Tương tự, khác biệt giữa các cung hoàng đạo không
                      có ý nghĩa thống kê rõ rệt.
                    </div>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>
          {/* END OF REPLACED BLOCK */}

          {/* Appendix & Downloads */}
          <TabsContent value="appendix" className="mt-6">
            <Section
              title="Phụ lục & Tải liệu"
              subtitle="Phương pháp, đặc tả biến và liên kết tải báo cáo gốc"
            >
              <div className="lg:col-span-7">
                <Card className="rounded-2xl">
                  <CardContent className="p-6 space-y-3 text-sm">
                    <div>
                      <h3 className="font-semibold">Phương pháp tóm tắt</h3>
                      <ul className="list-disc ml-5 space-y-1">
                        <li>
                          Mô hình: Linear Regression / Random Forest / Gradient
                          Boosting. So sánh trên tập test bằng R² & RMSE.
                        </li>
                        <li>
                          Giải thích mô hình: sử dụng SHAP để xếp hạng mức độ
                          quan trọng đặc trưng (Toán cao nhất).
                        </li>
                        <li>
                          So sánh nhóm: ANOVA & post-hoc (khi áp dụng) cho nhóm
                          tuổi và xu hướng học.
                        </li>
                      </ul>
                    </div>
                    <div>
                      <h3 className="font-semibold">Đặc tả dữ liệu</h3>
                      <ul className="list-disc ml-5 space-y-1">
                        <li>
                          Các môn: Toán, Văn, Anh, Lý, Hóa, Sinh, Sử, Địa,
                          GDCD/KTPL.
                        </li>
                        <li>Nhóm tuổi: 18, &gt;18, Thi lại.</li>
                        <li>
                          Trường hợp thiếu dữ liệu tháng sinh sẽ không vẽ được
                          RAE.
                        </li>
                      </ul>
                    </div>
                    <div>
                      <h1 className="font-semibold mb-2">
                        Tải báo cáo gốc (PDF) và tập dữ liệu (CSV)
                      </h1>
                      <span> Liên hệ email:</span>
                      <span className="font-bold">
                        {" "}
                        khang.vohuu@hcmut.edu.vn
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </Section>
          </TabsContent>
        </Tabs>

        <Button
          variant="destructive"
          className="fixed bottom-4 right-4 z-50 rounded-2xl text-black shadow-lg transition-all duration-300 hover:scale-110 hover:shadow-xl"
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        >
          <ArrowUp className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
