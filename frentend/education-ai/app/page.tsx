"use client";

import { useEffect, useState } from "react";
import {
  api,
  type ApiStudent,
  type AttendanceRecord,
  type AttendanceStudent,
  type Grade,
  type Course,
  type Exercise,
  type Submission,
  type StudentNotification,
  type Teacher,
  type TeacherCourse,
  type TeacherExercise,
  type TeacherNotification,
} from "../lib/api";
import {
  BarChart3,
  Bell,
  BookOpen,
  CalendarDays,
  Check,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  Download,
  Eye,
  EyeOff,
  GraduationCap,
  LayoutDashboard,
  LogOut,
  Menu,
  MoreHorizontal,
  Pencil,
  Plus,
  Search,
  Settings,
  ShieldCheck,
  Sparkles,
  Users,
  X,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type Role = "Student" | "Teacher" | "Admin";

const blue = "#0052CC";

let students = [
  {
    name: "Amine El Idrissi",
    email: "amine.elidrissi@edu.ma",
    className: "3AC",
    status: "Active",
    initials: "AE",
  },
  {
    name: "Salma Benali",
    email: "salma.benali@edu.ma",
    className: "3AC",
    status: "Active",
    initials: "SB",
  },
  {
    name: "Youssef Alaoui",
    email: "youssef.alaoui@edu.ma",
    className: "3AC",
    status: "Active",
    initials: "YA",
  },
  {
    name: "Nour El Amrani",
    email: "nour.elamrani@edu.ma",
    className: "1BAC",
    status: "Active",
    initials: "NE",
  },
  {
    name: "Aya Tazi",
    email: "aya.tazi@edu.ma",
    className: "1BAC",
    status: "Inactive",
    initials: "AT",
  },
];

type AdminStudent = (typeof students)[number];
type AdminTeacher = {
  teacher_id: number;
  full_name: string;
  email: string;
  classes: { class_id: number; name: string; academic_year: string }[];
};
type AdminClass = { class_id: number; name: string; academic_year: string };

let courses = [
  {
    name: "Algebra & Functions",
    teacher: "Nadia Bennani",
    exercises: [
      { name: "Exercise 1 — Equations", score: "18 / 20", state: "Submitted" },
      { name: "Exercise 2 — Functions", score: "—", state: "Not submitted" },
      {
        name: "Exercise 3 — Inequalities",
        score: "16 / 20",
        state: "Submitted",
      },
    ],
  },
  {
    name: "Geometry in Space",
    teacher: "Nadia Bennani",
    exercises: [
      { name: "Exercise 1 — Vectors", score: "19 / 20", state: "Submitted" },
      { name: "Exercise 2 — Planes", score: "—", state: "Not submitted" },
    ],
  },
  {
    name: "Probability",
    teacher: "Karim Rami",
    exercises: [
      { name: "Exercise 1 — Events", score: "17 / 20", state: "Submitted" },
    ],
  },
];

function Avatar({
  initials,
  className = "",
}: {
  initials: string;
  className?: string;
}) {
  return (
    <div
      className={`flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-[#0052CC] ${className}`}
    >
      {initials}
    </div>
  );
}

function Sidebar({
  role,
  open,
  setOpen,
  active,
  userName,
  onLogout,
  setActive,
}: {
  role: Role;
  open: boolean;
  setOpen: (value: boolean) => void;
  active: string;
  userName: string;
  onLogout: () => void;
  setActive: (value: string) => void;
}) {
  const items =
    role === "Student"
      ? [
          ["Overview", LayoutDashboard],
          ["My Courses", BookOpen],
          ["Progress", BarChart3],
          ["Announcements", Bell],
        ]
      : role === "Teacher"
        ? [
            ["Overview", LayoutDashboard],
            ["Submissions", ClipboardCheck],
            ["Attendance", CalendarDays],
            ["My Classes", Users],
          ]
        : [
            ["Overview", LayoutDashboard],
            ["Students", GraduationCap],
            ["Teachers", Users],
            ["Classes", BookOpen],
            ["Reports", BarChart3],
          ];
  return (
    <>
      {open && (
        <button
          aria-label="Close navigation"
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-30 bg-slate-950/20 lg:hidden"
        />
      )}
      <aside
        className={`fixed inset-y-0 left-0 z-40 flex w-[250px] flex-col border-r border-[#E2E8F0] bg-white text-[#334155] transition-transform lg:static lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}
      >
        <div className="flex h-20 items-center gap-3 border-b border-[#E2E8F0] px-6">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#0052CC] text-white">
            <BookOpen size={18} />
          </div>
          <div>
            <div className="font-bold tracking-tight text-[#0F172A]">
              EduInsight <span className="text-[#0052CC]">AI</span>
            </div>
            <div className="text-[10px] uppercase tracking-[.22em] text-[#64748B]">
              AI-Powered Learning Platform
            </div>
          </div>
          <button
            className="ml-auto text-[#334155] lg:hidden"
            onClick={() => setOpen(false)}
          >
            <X size={18} />
          </button>
        </div>
        <div className="px-4 pt-6">
          <div className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[.2em] text-[#64748B]">
            Workspace
          </div>
          {items.map(([label, Icon]) => (
            <button
              key={label as string}
              onClick={() => {
                const section =
                  label === "Overview"
                    ? "overview"
                    : (label as string).toLowerCase().replaceAll(" ", "-");
                setActive(label as string);
                document
                  .getElementById(section)
                  ?.scrollIntoView({ behavior: "smooth" });
                setOpen(false);
              }}
              className={`mb-1 flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm transition ${active === label ? "bg-[#EFF6FF] font-semibold text-[#0052CC]" : "text-[#334155] hover:bg-[#F8FAFC] hover:text-[#0052CC]"}`}
            >
              <Icon size={17} />
              <span>{label as string}</span>
              {label === "Announcements" && (
                <span className="ml-auto rounded-full bg-[#0052CC] px-2 py-0.5 text-[10px] text-white">
                  3
                </span>
              )}
            </button>
          ))}
        </div>
        <div className="mt-auto border-t border-[#E2E8F0] p-4">
          <div className="flex items-center gap-3">
            <Avatar
              initials={
                userName
                  .split(" ")
                  .map((part) => part[0])
                  .join("")
                  .slice(0, 2)
                  .toUpperCase() || "U"
              }
            />
            <div className="min-w-0">
              <p className="truncate text-xs font-semibold text-[#0F172A]">
                {userName}
              </p>
              <p className="text-[10px] text-[#64748B]">{role} Account</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg border border-[#DBEAFE] px-3 py-2 text-xs font-semibold text-[#0052CC] hover:bg-[#EFF6FF]"
          >
            <LogOut size={14} /> Logout
          </button>
        </div>
      </aside>
    </>
  );
}

function Topbar({
  role,
  setOpen,
  onLogout,
  userName,
  notifications,
}: {
  role: Role;
  setOpen: (value: boolean) => void;
  onLogout: () => void;
  userName: string;
  notifications: TeacherNotification[];
}) {
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  return (
    <header className="relative flex min-h-20 items-center justify-between border-b border-[#DBEAFE] bg-white px-3 pb-3 pt-7 sm:px-5 md:px-8 lg:pt-3">
      <div className="flex min-w-0 items-center gap-2.5">
        <button
          aria-label="Open navigation"
          onClick={() => setOpen(true)}
          className="shrink-0 rounded-lg p-2 text-[#0052CC] hover:bg-[#EFF6FF] lg:hidden"
        >
          <Menu size={20} />
        </button>
        <div className="min-w-0">
          <div className="truncate text-[10px] font-bold uppercase tracking-[.14em] text-[#64748B] sm:text-xs">
            {role} workspace
          </div>
          <h1 className="truncate text-base font-bold text-[#0F172A] sm:text-xl">
            {userName}
          </h1>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <button
          aria-label="Notifications"
          onClick={() => setNotificationsOpen((value) => !value)}
          className="relative rounded-xl border border-[#DBEAFE] p-2.5 text-[#475569] hover:bg-[#EFF6FF]"
        >
          <Bell size={18} />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-[#0052CC]" />
        </button>
        {notificationsOpen && (
          <div className="absolute right-24 top-16 z-50 w-80 rounded-xl border border-[#DBEAFE] bg-white p-4 shadow-lg">
            <h3 className="font-bold text-[#0F172A]">Notifications</h3>
            {notifications.length ? (
              notifications.map((notification) => (
                <div
                  key={notification.notification_id}
                  className="border-b border-slate-50 py-3"
                >
                  <p className="text-sm font-semibold text-slate-800">
                    {notification.title}
                  </p>
                  <p className="mt-1 text-xs text-[#64748B]">
                    {notification.message}
                  </p>
                </div>
              ))
            ) : (
              <p className="py-5 text-sm text-[#64748B]">
                No new notifications
              </p>
            )}
          </div>
        )}
        <button
          onClick={onLogout}
          className="hidden items-center gap-2 rounded-xl border border-[#DBEAFE] px-3 py-2 text-xs font-semibold text-[#0052CC] hover:bg-[#EFF6FF] sm:flex"
        >
          <LogOut size={14} /> Logout
        </button>
      </div>
    </header>
  );
}

function Stat({
  label,
  value,
  detail,
  icon: Icon,
}: {
  label: string;
  value: string;
  detail?: string;
  icon: any;
}) {
  return (
    <div className="rounded-2xl border border-[#DBEAFE] bg-white p-3.5 shadow-[0_2px_12px_rgba(29,78,216,.06)] sm:p-5">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="truncate text-[11px] font-semibold text-[#475569] sm:text-xs">
            {label}
          </p>
          <p className="mt-1.5 text-xl font-bold tracking-tight text-[#0F172A] sm:mt-2 sm:text-2xl">
            {value}
          </p>
          {detail && (
            <p className="mt-1 truncate text-[10px] text-[#475569] sm:text-xs">
              {detail}
            </p>
          )}
        </div>
        <div className="shrink-0 rounded-xl bg-[#EFF6FF] p-2 text-[#1D4ED8] sm:p-2.5">
          <Icon size={18} />
        </div>
      </div>
    </div>
  );
}

/* Legacy mock student dashboard retained only as historical markup; the active route uses ClassicStudentWorkspace.
function StudentDashboard() {
  const [subject, setSubject] = useState("Math · 3AC");
  const [tab, setTab] = useState<"Courses" | "Classmates">("Courses");
  return (
    <div className="space-y-4 sm:space-y-7">
      <div className="flex flex-col justify-between gap-3 md:flex-row md:items-end">
        <div className="flex items-center justify-between gap-3">
          <p className="text-xs font-semibold text-[#475569] sm:text-sm">
            Active classroom
          </p>
          <div className="relative">
            <select
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="appearance-none rounded-xl border border-[#DBEAFE] bg-white py-2.5 pl-3 pr-9 text-xs font-bold text-[#0F172A] outline-none focus:border-[#2563EB] focus:ring-2 focus:ring-[#DBEAFE] sm:py-3 sm:pl-4 sm:pr-12 sm:text-sm"
            >
              <option>Math · 3AC</option>
              <option>Physics · 3AC</option>
              <option>French · 3AC</option>
            </select>
            <ChevronDown
              className="pointer-events-none absolute right-4 top-3.5 text-[#475569]"
              size={16}
            />
          </div>
        </div>
        <div className="flex items-center rounded-xl border border-[#DBEAFE] bg-white px-3 py-2.5 text-[11px] text-[#1E3A8A] sm:px-4 sm:py-3 sm:text-xs">
          <span className="mr-1 font-bold text-[#1D4ED8]">Next:</span>
          <span className="truncate">Exercise 2 — Functions</span>
          <span className="ml-auto shrink-0 pl-2 font-semibold text-[#475569]">
            Tomorrow
          </span>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 sm:gap-4">
        <Stat
          label="Average score"
          value="17.5 / 20"
          detail="+1.2 this month"
          icon={BarChart3}
        />
        <Stat
          label="Exercises done"
          value="12 / 15"
          detail="80% completion"
          icon={ClipboardCheck}
        />
        <Stat
          label="Class rank"
          value="#4"
          detail="of 28 students"
          icon={GraduationCap}
        />
      </div>
      <div className="grid gap-5 xl:grid-cols-[1.6fr_1fr]">
        <section className="rounded-2xl border border-[#DBEAFE] bg-white">
          <div className="flex items-center justify-between border-b border-[#DBEAFE] px-5 py-4">
            <div>
              <h2 className="font-bold text-[#0F172A]">
                {subject.split(" · ")[0]} learning path
              </h2>
              <p className="mt-1 text-xs text-[#475569]">
                Courses and exercises for this class
              </p>
            </div>
            <div className="flex gap-1 rounded-lg bg-[#EFF6FF] p-1">
              {(["Courses", "Classmates"] as const).map((item) => (
                <button
                  onClick={() => setTab(item)}
                  key={item}
                  className={`rounded-md px-3 py-1.5 text-xs font-semibold ${tab === item ? "bg-white text-[#0052CC] shadow-sm" : "text-[#475569]"}`}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
          {tab === "Courses" ? (
            <div className="space-y-3 p-5">
              {courses.map((course) => (
                <div
                  key={course.name}
                  className="rounded-xl border border-[#DBEAFE]"
                >
                  <div className="flex items-center gap-3 bg-white/70 px-4 py-3">
                    <div className="rounded-lg bg-blue-100 p-2 text-[#0052CC]">
                      <BookOpen size={16} />
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-slate-800">
                        {course.name}
                      </h3>
                      <p className="text-[11px] text-[#475569]">
                        with {course.teacher}
                      </p>
                    </div>
                    <span className="ml-auto text-xs text-[#475569]">
                      {course.exercises.length} exercises
                    </span>
                  </div>
                  {course.exercises.map((ex) => (
                    <div
                      key={ex.name}
                      className="flex items-center gap-3 border-t border-[#DBEAFE] px-4 py-3"
                    >
                      <div
                        className={`h-2 w-2 rounded-full ${ex.state === "Submitted" ? "bg-emerald-500" : "bg-slate-300"}`}
                      />
                      <p className="text-xs font-medium text-slate-700">
                        {ex.name}
                      </p>
                      <span
                        className={`ml-auto rounded-full px-2 py-1 text-[10px] font-semibold ${ex.state === "Submitted" ? "bg-emerald-50 text-emerald-700" : "bg-[#EFF6FF] text-[#475569]"}`}
                      >
                        {ex.state}
                      </span>
                      <span className="w-14 text-right text-xs font-bold text-slate-700">
                        {ex.score}
                      </span>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          ) : (
            <div className="grid gap-2 p-5 sm:grid-cols-2">
              {students.slice(0, 4).map((student) => (
                <div
                  key={student.name}
                  className="flex items-center gap-3 rounded-xl border border-[#DBEAFE] p-3"
                >
                  <Avatar initials={student.initials} />
                  <div>
                    <p className="text-xs font-semibold text-slate-800">
                      {student.name}
                    </p>
                    <p className="text-[11px] text-[#475569]">Classmate</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
        <aside className="space-y-5">
          <section className="rounded-2xl bg-[#0c2254] p-5 text-white">
            <div className="flex items-center gap-2 text-blue-200">
              <Bell size={16} />
              <span className="text-xs font-semibold uppercase tracking-[.15em]">
                Announcement
              </span>
            </div>
            <h3 className="mt-5 text-lg font-bold">Mock exam schedule</h3>
            <p className="mt-2 text-sm leading-6 text-blue-100/75">
              The mathematics mock exam will take place on Friday, April 26 at
              09:00.
            </p>
            <button className="mt-5 text-xs font-bold text-white underline underline-offset-4">
              Read all announcements
            </button>
          </section>
          <section className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
            <div className="flex items-center justify-between">
              <h2 className="font-bold text-[#0F172A]">Recent feedback</h2>
              <button className="text-xs font-semibold text-[#0052CC]">
                View all
              </button>
            </div>
            <div className="mt-4 space-y-4">
              <div className="flex gap-3">
                <Avatar initials="NB" />
                <div>
                  <p className="text-xs font-semibold text-slate-800">
                    Nadia Bennani
                  </p>
                  <p className="mt-1 text-xs leading-5 text-[#475569]">
                    “Great progress on your last exercise. Keep showing your
                    work.”
                  </p>
                </div>
              </div>
              <div className="flex gap-3">
                <Avatar initials="KR" />
                <div>
                  <p className="text-xs font-semibold text-slate-800">
                    Karim Rami
                  </p>
                  <p className="mt-1 text-xs leading-5 text-[#475569]">
                    “Your reasoning is becoming much clearer.”
                  </p>
                </div>
              </div>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}
*/

function DynamicTeacherWorkspace({
  active,
  teacher,
  students,
  courses,
  exercises,
  grades,
  attendance,
  onAttendanceSaved,
}: {
  active: string;
  teacher: Teacher;
  students: AttendanceStudent[];
  courses: TeacherCourse[];
  exercises: TeacherExercise[];
  grades: Grade[];
  attendance: AttendanceRecord[];
  onAttendanceSaved: () => void;
}) {
  const [classId, setClassId] = useState(teacher.classes[0]?.class_id ?? 0);
  const [exerciseId, setExerciseId] = useState(exercises[0]?.exercise_id ?? 0);
  const [statuses, setStatuses] = useState<
    Record<number, "present" | "absent">
  >(() =>
    Object.fromEntries(
      students.map((student) => [student.student_id, "absent"]),
    ),
  );
  const [saving, setSaving] = useState(false);
  const selectedStudents = students.filter(
    (student) => student.class_id === classId,
  );
  const selectedExercise = exercises.find(
    (exercise) => exercise.exercise_id === exerciseId,
  );
  const today = new Date().toISOString().slice(0, 10);
  const todayAttendance = attendance.filter(
    (record) => record.date === today && record.class_id === classId,
  );
  const presentCount = todayAttendance.filter(
    (record) => record.status === "present",
  ).length;
  const attendancePercent = selectedStudents.length
    ? Math.round((presentCount / selectedStudents.length) * 100)
    : 0;

  useEffect(() => {
    const current = Object.fromEntries(
      students.map((student) => [student.student_id, "absent"] as const),
    );
    attendance
      .filter((record) => record.date === today && record.class_id === classId)
      .forEach((record) => {
        current[record.student_id] = record.status;
      });
    setStatuses(current);
  }, [students, attendance, classId, today]);

  const saveAttendance = async () => {
    setSaving(true);
    try {
      await api.saveAttendance(
        classId,
        today,
        selectedStudents.map((student) => ({
          student_id: student.student_id,
          status: statuses[student.student_id] ?? "absent",
        })),
      );
      onAttendanceSaved();
    } finally {
      setSaving(false);
    }
  };

  if (active === "My Classes")
    return (
      <section id="my-classes" className="space-y-5">
        <h2 className="text-2xl font-bold text-[#0F172A]">My Classes</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {teacher.classes.length ? (
            teacher.classes.map((item) => (
              <button
                key={item.class_id}
                onClick={() => setClassId(item.class_id)}
                className={`rounded-2xl border p-5 text-left ${classId === item.class_id ? "border-[#0052CC] bg-[#EFF6FF]" : "border-[#DBEAFE] bg-white"}`}
              >
                <BookOpen className="mb-3 text-[#0052CC]" size={20} />
                <p className="font-bold text-[#0F172A]">{item.name}</p>
                <p className="mt-1 text-xs text-[#64748B]">
                  {item.academic_year}
                </p>
              </button>
            ))
          ) : (
            <p className="text-sm text-[#64748B]">No classes assigned.</p>
          )}
        </div>
      </section>
    );

  if (active === "Attendance")
    return (
      <section id="attendance" className="space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-2xl font-bold text-[#0F172A]">Attendance</h2>
            <p className="mt-1 text-sm text-[#64748B]">
              {today} · {attendancePercent}% present
            </p>
          </div>
          <select
            value={classId}
            onChange={(event) => setClassId(Number(event.target.value))}
            className="rounded-xl border border-[#DBEAFE] px-3 py-2 text-sm"
          >
            {teacher.classes.map((item) => (
              <option key={item.class_id} value={item.class_id}>
                {item.name}
              </option>
            ))}
          </select>
        </div>
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          {selectedStudents.length ? (
            selectedStudents.map((student) => (
              <div
                key={student.student_id}
                className="flex items-center gap-3 border-b border-slate-50 py-3"
              >
                <Avatar
                  initials={student.full_name
                    .split(" ")
                    .map((part) => part[0])
                    .join("")
                    .slice(0, 2)}
                />
                <span className="flex-1 text-sm font-semibold text-slate-700">
                  {student.full_name}
                </span>
                <button
                  onClick={() =>
                    setStatuses({
                      ...statuses,
                      [student.student_id]:
                        statuses[student.student_id] === "present"
                          ? "absent"
                          : "present",
                    })
                  }
                  className={`rounded-full px-3 py-1.5 text-xs font-bold ${statuses[student.student_id] === "present" ? "bg-emerald-50 text-emerald-700" : "bg-rose-50 text-rose-600"}`}
                >
                  {statuses[student.student_id] === "present"
                    ? "Present"
                    : "Absent"}
                </button>
              </div>
            ))
          ) : (
            <p className="text-sm text-[#64748B]">
              No students enrolled in this class.
            </p>
          )}
          <button
            onClick={saveAttendance}
            disabled={saving || !classId}
            className="mt-4 rounded-xl bg-[#0052CC] px-4 py-3 text-xs font-bold text-white disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save attendance"}
          </button>
        </div>
      </section>
    );

  if (active === "Submissions")
    return (
      <section id="submissions" className="space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-2xl font-bold text-[#0F172A]">
              Submissions & Grading
            </h2>
            <p className="mt-1 text-sm text-[#64748B]">
              Real students and grades from the backend.
            </p>
          </div>
          <select
            value={exerciseId}
            onChange={(event) => setExerciseId(Number(event.target.value))}
            className="rounded-xl border border-[#DBEAFE] px-3 py-2 text-sm"
          >
            {exercises.map((item) => (
              <option key={item.exercise_id} value={item.exercise_id}>
                {item.exercise_name}
              </option>
            ))}
          </select>
        </div>
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          {selectedExercise && selectedStudents.length ? (
            selectedStudents.map((student) => {
              const grade = grades.find(
                (item) =>
                  item.student_id === student.student_id &&
                  item.exercise_id === selectedExercise.exercise_id,
              );
              return (
                <div
                  key={student.student_id}
                  className="flex items-center gap-3 border-b border-slate-50 py-3"
                >
                  <Avatar
                    initials={student.full_name
                      .split(" ")
                      .map((part) => part[0])
                      .join("")
                      .slice(0, 2)}
                  />
                  <span className="flex-1 text-sm font-semibold text-slate-700">
                    {student.full_name}
                  </span>
                  <span className="text-sm font-bold text-[#0052CC]">
                    {grade ? grade.score : "-"} / {selectedExercise.max_score}
                  </span>
                </div>
              );
            })
          ) : (
            <p className="text-sm text-[#64748B]">
              No submissions or exercises available.
            </p>
          )}
        </div>
      </section>
    );

  return (
    <section id="overview" className="space-y-7">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="mb-2 text-sm text-[#475569]">Active class</p>
          <select
            value={classId}
            onChange={(event) => setClassId(Number(event.target.value))}
            className="rounded-xl border border-[#DBEAFE] bg-white px-4 py-3 text-sm font-semibold text-slate-800"
          >
            {teacher.classes.map((item) => (
              <option key={item.class_id} value={item.class_id}>
                {item.name}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <Stat
          label="Class students"
          value={String(selectedStudents.length)}
          icon={Users}
        />
        <Stat
          label="Exercises"
          value={String(exercises.length)}
          icon={ClipboardCheck}
        />
        <Stat
          label="Attendance today"
          value={`${attendancePercent}%`}
          icon={CalendarDays}
        />
      </div>
      <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
        <h2 className="font-bold text-[#0F172A]">Classes and courses</h2>
        {courses.length ? (
          courses.map((course) => (
            <div
              key={course.course_id}
              className="flex justify-between border-b border-slate-50 py-3 text-sm"
            >
              <span className="font-semibold text-slate-700">
                {course.course_name}
              </span>
              <span className="text-[#64748B]">{course.level}</span>
            </div>
          ))
        ) : (
          <p className="mt-3 text-sm text-[#64748B]">No courses available.</p>
        )}
      </div>
    </section>
  );
}

/* Legacy mock teacher dashboard retained only as historical markup; the active route uses DynamicTeacherWorkspace.
function TeacherDashboard() {
  const [className, setClassName] = useState("3AC Math");
  const [classId, setClassId] = useState<number | null>(null);
  const [savingAttendance, setSavingAttendance] = useState(false);
  const [grade, setGrade] = useState<Record<string, string>>({
    "Amine El Idrissi": "18",
    "Salma Benali": "16",
    "Youssef Alaoui": "19",
  });
  const [attendance, setAttendance] = useState<Record<string, boolean>>({
    "Amine El Idrissi": true,
    "Salma Benali": true,
    "Youssef Alaoui": false,
    "Nour El Amrani": true,
  });
  const roster = students.slice(0, 4);
  useEffect(() => {
    api
      .getTeacher()
      .then((teacher) => {
        setClassId(teacher.classes[0]?.class_id ?? null);
        setClassName(teacher.classes[0]?.name ?? "No assigned class");
      })
      .catch(() => undefined);
  }, []);

  const saveAttendance = async () => {
    if (!classId || !roster.length) return;
    setSavingAttendance(true);
    try {
      await api.saveAttendance(
        classId,
        new Date().toISOString().slice(0, 10),
        roster.map((student) => ({
          student_id: Number(
            (student as typeof student & { student_id?: number }).student_id,
          ),
          status: attendance[student.name] ? "present" : "absent",
        })),
      );
    } finally {
      setSavingAttendance(false);
    }
  };
  return (
    <div id="overview" className="space-y-7">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div id="my-classes">
          <p className="mb-2 text-sm text-[#475569]">Active class</p>
          <div className="relative">
            <select
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              className="appearance-none rounded-xl border border-[#DBEAFE] bg-white py-3 pl-4 pr-12 text-sm font-semibold text-slate-800"
            >
              <option>3AC Math</option>
              <option>1BAC Physics</option>
            </select>
            <ChevronDown
              className="pointer-events-none absolute right-4 top-3.5 text-[#475569]"
              size={16}
            />
          </div>
        </div>
        <button className="flex items-center gap-2 self-start rounded-xl bg-[#0052CC] px-4 py-3 text-xs font-bold text-white shadow-sm hover:bg-blue-800">
          <Plus size={15} /> Create exercise
        </button>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <Stat
          label="Class average"
          value="15.8 / 20"
          detail="Across 28 students"
          icon={BarChart3}
        />
        <Stat
          label="To grade"
          value="8"
          detail="Submissions pending"
          icon={ClipboardCheck}
        />
        <Stat
          label="Attendance today"
          value="92%"
          detail="26 present · 2 absent"
          icon={CalendarDays}
        />
      </div>
      <div className="grid gap-5 xl:grid-cols-[1.55fr_1fr]">
        <section
          id="submissions"
          className="rounded-2xl border border-[#DBEAFE] bg-white"
        >
          <div className="flex flex-col justify-between gap-3 border-b border-[#DBEAFE] px-5 py-4 md:flex-row md:items-center">
            <div>
              <h2 className="font-bold text-[#0F172A]">Submissions</h2>
              <p className="mt-1 text-xs text-[#475569]">
                Exercise 1 — Equations · {className}
              </p>
            </div>
            <div className="flex gap-2">
              <select className="rounded-lg border border-[#DBEAFE] px-2 py-2 text-xs text-slate-600">
                <option>Algebra</option>
                <option>Geometry</option>
              </select>
              <select className="rounded-lg border border-[#DBEAFE] px-2 py-2 text-xs text-slate-600">
                <option>Exercise 1</option>
                <option>Exercise 2</option>
              </select>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-[#DBEAFE] text-[10px] uppercase tracking-wider text-[#475569]">
                  <th className="px-5 py-3 font-semibold">Student</th>
                  <th className="px-3 py-3 font-semibold">Submitted</th>
                  <th className="px-3 py-3 font-semibold">Grade / 20</th>
                  <th className="px-5 py-3" />
                </tr>
              </thead>
              <tbody>
                {roster.slice(0, 3).map((student) => (
                  <tr
                    key={student.name}
                    className="border-b border-slate-50 last:border-0"
                  >
                    <td className="px-5 py-3">
                      <div className="flex items-center gap-2.5">
                        <Avatar
                          initials={student.initials}
                          className="h-8 w-8 text-[10px]"
                        />
                        <span className="text-xs font-semibold text-slate-700">
                          {student.name}
                        </span>
                      </div>
                    </td>
                    <td className="px-3 py-3 text-xs text-[#475569]">
                      Today, 09:24
                    </td>
                    <td className="px-3 py-3">
                      <input
                        aria-label={`Grade for ${student.name}`}
                        value={grade[student.name] ?? ""}
                        onChange={(e) => {
                          const value = e.target.value;
                          if (+value <= 20)
                            setGrade({ ...grade, [student.name]: value });
                        }}
                        className="w-14 rounded-lg border border-[#DBEAFE] px-2 py-1.5 text-xs font-bold text-slate-800 outline-none focus:border-blue-500"
                      />
                    </td>
                    <td className="px-5 py-3 text-right">
                      <button className="rounded-lg p-2 text-[#475569] hover:bg-white hover:text-[#0052CC]">
                        <Pencil size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
        <section
          id="attendance"
          className="rounded-2xl border border-[#DBEAFE] bg-white"
        >
          <div className="border-b border-[#DBEAFE] px-5 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-bold text-[#0F172A]">Attendance</h2>
                <p className="mt-1 text-xs text-[#475569]">
                  Thursday, April 18, 2024
                </p>
              </div>
              <button className="rounded-lg border border-[#DBEAFE] p-2 text-[#475569]">
                <CalendarDays size={15} />
              </button>
            </div>
            <button
              onClick={saveAttendance}
              disabled={savingAttendance || !classId}
              className="mt-3 rounded-lg bg-[#0052CC] px-3 py-2 text-xs font-bold text-white disabled:opacity-50"
            >
              {savingAttendance ? "Saving..." : "Save attendance"}
            </button>
          </div>
          <div className="space-y-2 p-5">
            {roster.map((student) => (
              <div key={student.name} className="flex items-center gap-3">
                <Avatar
                  initials={student.initials}
                  className="h-8 w-8 text-[10px]"
                />
                <span className="min-w-0 flex-1 truncate text-xs font-semibold text-slate-700">
                  {student.name}
                </span>
                <button
                  onClick={() =>
                    setAttendance({
                      ...attendance,
                      [student.name]: !attendance[student.name],
                    })
                  }
                  className={`rounded-full px-3 py-1.5 text-[10px] font-bold ${attendance[student.name] ? "bg-emerald-50 text-emerald-700" : "bg-rose-50 text-rose-600"}`}
                >
                  {attendance[student.name] ? "Present" : "Absent"}
                </button>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

*/

function AdminDashboard({
  students,
  teachers,
  classes,
}: {
  students: AdminStudent[];
  teachers: AdminTeacher[];
  classes: AdminClass[];
}) {
  const [tab, setTab] = useState("Students");
  const [query, setQuery] = useState("");
  const filtered = students.filter(
    (s) =>
      s.name.toLowerCase().includes(query.toLowerCase()) ||
      s.email.toLowerCase().includes(query.toLowerCase()),
  );
  return (
    <div className="space-y-7">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="text-sm text-[#475569]">
            Manage your learning community
          </p>
          <h2 className="mt-1 text-2xl font-bold tracking-tight text-[#0F172A]">
            People & classes
          </h2>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 rounded-xl border border-[#DBEAFE] px-4 py-3 text-xs font-bold text-slate-700">
            <Download size={15} /> Export records
          </button>
          <button className="flex items-center gap-2 rounded-xl bg-[#0052CC] px-4 py-3 text-xs font-bold text-white">
            <Plus size={15} /> Add {tab.slice(0, -1)}
          </button>
        </div>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <Stat
          label="Total students"
          value={String(students.length)}
          icon={GraduationCap}
        />
        <Stat
          label="Teaching staff"
          value={String(teachers.length)}
          icon={Users}
        />
        <Stat
          label="Active classes"
          value={String(classes.length)}
          icon={BookOpen}
        />
      </div>
      <div className="rounded-2xl border border-[#DBEAFE] bg-white">
        <div className="flex flex-col justify-between gap-4 border-b border-[#DBEAFE] p-5 md:flex-row md:items-center">
          <div className="flex gap-1 rounded-lg bg-[#EFF6FF] p-1">
            {["Students", "Teachers", "Classes"].map((item) => (
              <button
                key={item}
                onClick={() => setTab(item)}
                className={`rounded-md px-4 py-2 text-xs font-bold ${tab === item ? "bg-white text-[#0052CC] shadow-sm" : "text-[#475569]"}`}
              >
                {item}
              </button>
            ))}
          </div>
          <div className="relative">
            <Search
              className="absolute left-3 top-2.5 text-[#475569]"
              size={15}
            />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={`Search ${tab.toLowerCase()}...`}
              className="w-full rounded-lg border border-[#DBEAFE] py-2 pl-9 pr-3 text-xs outline-none focus:border-blue-500 md:w-64"
            />
          </div>
        </div>
        {tab === "Students" ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-[#DBEAFE] text-[10px] uppercase tracking-wider text-[#475569]">
                  <th className="px-5 py-3">Student</th>
                  <th className="px-3 py-3">Class</th>
                  <th className="px-3 py-3">Status</th>
                  <th className="px-5 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((student) => (
                  <tr
                    key={student.email}
                    className="border-b border-slate-50 last:border-0"
                  >
                    <td className="px-5 py-3">
                      <div className="flex items-center gap-3">
                        <Avatar initials={student.initials} />
                        <div>
                          <p className="text-xs font-semibold text-slate-800">
                            {student.name}
                          </p>
                          <p className="text-[11px] text-[#475569]">
                            {student.email}
                          </p>
                        </div>
                      </div>
                    </td>
                    <td className="px-3 py-3 text-xs font-medium text-slate-600">
                      {student.className}
                    </td>
                    <td className="px-3 py-3">
                      <span
                        className={`rounded-full px-2 py-1 text-[10px] font-bold ${student.status === "Active" ? "bg-emerald-50 text-emerald-700" : "bg-[#EFF6FF] text-[#475569]"}`}
                      >
                        {student.status}
                      </span>
                    </td>
                    <td className="px-5 py-3 text-right">
                      <button className="rounded-lg p-2 text-[#475569] hover:bg-white">
                        <MoreHorizontal size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="grid gap-3 p-5 sm:grid-cols-2">
            {(tab === "Teachers" ? teachers : classes).map((item) => (
              <div
                key={item}
                className="flex items-center gap-3 rounded-xl border border-[#DBEAFE] p-4"
              >
                <div className="rounded-xl bg-blue-50 p-2.5 text-[#0052CC]">
                  {tab === "Teachers" ? (
                    <Users size={17} />
                  ) : (
                    <BookOpen size={17} />
                  )}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-semibold text-slate-800">
                    {"full_name" in item ? item.full_name : item.name}
                  </p>
                  <p className="text-xs text-[#475569]">
                    {"full_name" in item
                      ? `${item.classes.length} assigned classes`
                      : item.academic_year}
                  </p>
                </div>
                <button className="rounded-lg p-2 text-[#475569] hover:bg-white">
                  <MoreHorizontal size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
      <section className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
        <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
          <div>
            <h2 className="font-bold text-[#0F172A]">
              Monthly attendance report
            </h2>
            <p className="mt-1 text-xs text-[#475569]">
              Review attendance trends across your classes.
            </p>
          </div>
          <div className="flex gap-2">
            <select className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-xs">
              <option>April 2024</option>
              <option>March 2024</option>
            </select>
            <button className="rounded-lg bg-blue-50 px-3 py-2 text-xs font-bold text-[#0052CC]">
              View report
            </button>
          </div>
        </div>
        <div className="mt-5 flex h-24 items-end gap-2">
          {[62, 78, 69, 84, 91, 86, 94, 88, 96, 90, 97, 93].map(
            (height, index) => (
              <div
                key={index}
                className="flex flex-1 flex-col items-center gap-1"
              >
                <div
                  style={{ height: `${height}%` }}
                  className="w-full rounded-t-md bg-blue-200 first:bg-[#0052CC]"
                />
                <span className="text-[9px] text-[#475569]">{index + 1}</span>
              </div>
            ),
          )}
        </div>
      </section>
    </div>
  );
}

function Login({ setRole }: { setRole: (role: Role) => void }) {
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    const form = new FormData(event.currentTarget);
    try {
      const response = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: form.get("email"),
          password: form.get("password"),
          rememberMe: form.get("rememberMe") === "on",
        }),
      });
      if (!response.ok) throw new Error("Invalid email or password");
      const data = await response.json();
      const role = String(data.role ?? data.user?.role ?? "").toLowerCase();
      if (role === "admin") window.location.href = "/admin";
      else if (role === "teacher") window.location.href = "/teacher";
      else if (role === "student") window.location.href = "/student";
      else throw new Error("Your account role could not be verified");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in");
    }
  };
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#F4F7FA] p-4 font-sans sm:p-5">
      <div className="grid w-full max-w-md overflow-hidden rounded-xl border border-[#CBD5E1] bg-white shadow-[0_2px_5px_rgba(15,23,42,.12)]">
        <div className="hidden">
          <img
            src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-0crM3hmoRRVMnLX5x57rgKCIYcb5gX.png"
            alt="Abstract blue and white wave pattern"
            className="absolute inset-0 h-full w-full object-cover opacity-35"
          />
          <div className="relative flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500">
              <Sparkles size={20} />
            </div>
            <span className="text-lg font-bold">
              EduInsight <span className="text-blue-300">AI</span>
            </span>
          </div>
          <div className="relative">
            <p className="mb-4 text-xs font-bold uppercase tracking-[.2em] text-blue-200">
              Learn smarter
            </p>
            <h1 className="max-w-sm text-4xl font-bold leading-tight">
              AI-powered learning for everyone.
            </h1>
            <p className="mt-5 max-w-sm text-sm leading-6 text-blue-100/75">
              One clear space for students, teachers, and the teams that support
              them.
            </p>
          </div>
          <p className="relative text-xs text-blue-100/60">
            © 2024 EduInsight AI
          </p>
        </div>
        <div className="p-7 sm:p-10">
          <div className="mb-8 text-center">
            <div className="mx-auto mb-4 flex h-[70px] w-[70px] items-center justify-center rounded-[18px] bg-[#0052CC] text-white shadow-sm">
              <BookOpen size={34} strokeWidth={2} />
            </div>
            <div className="text-[29px] font-bold tracking-[-0.04em] text-[#07152F]">
              EduInsight AI
            </div>
            <p className="mt-2 text-[17px] text-[#64748B]">
              AI-Powered Learning Platform
            </p>
          </div>
          <p className="text-[22px] font-bold tracking-[-0.02em] text-[#07152F]">
            Welcome back
          </p>
          <h2 className="mt-2 text-[18px] font-normal text-[#526681]">
            Sign in to your account
          </h2>
          <form onSubmit={handleSubmit} className="mt-7 space-y-4">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-[#0F172A]">
                Email
              </label>
              <input
                type="email"
                required
                name="email"
                placeholder="user@eduinsight.ai"
                className="w-full rounded-lg border border-[#DBEAFE] bg-[#F3F6F9] px-4 py-3 text-sm text-[#0F172A] outline-none placeholder:text-[#64748B] focus:border-[#0052CC] focus:ring-2 focus:ring-[#BFDBFE]"
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-[#0F172A]">
                Password
              </label>
              <div className="relative">
                <input
                  name="password"
                  type={showPassword ? "text" : "password"}
                  required
                  placeholder="••••••••"
                  className="w-full rounded-lg border border-[#DBEAFE] bg-[#F3F6F9] px-4 py-3 text-sm text-[#0F172A] outline-none placeholder:text-[#64748B] focus:border-[#0052CC] focus:ring-2 focus:ring-[#BFDBFE] pr-11"
                />
                <button
                  type="button"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  onClick={() => setShowPassword((value) => !value)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-[#64748B]"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>
            <div className="flex items-center justify-between gap-3 text-xs">
              <label className="flex items-center gap-2 text-[#475569]">
                <input
                  name="rememberMe"
                  type="checkbox"
                  className="rounded border-[#CBD5E1] text-[#0052CC]"
                />{" "}
                Remember me
              </label>
              <button
                type="button"
                className="font-semibold text-[#2563EB] hover:underline"
              >
                Forgot password?
              </button>
            </div>
            {error && (
              <p role="alert" className="text-sm font-medium text-red-600">
                {error}
              </p>
            )}
            <button
              type="submit"
              className="w-full rounded-lg bg-[#0052CC] py-3 text-sm font-bold text-white transition hover:bg-[#1D4ED8]"
            >
              Sign In
            </button>
          </form>
          <div className="hidden mt-8 space-y-3">
            {(["Student", "Teacher", "Admin"] as Role[]).map((role) => (
              <button
                onClick={() => setRole(role)}
                key={role}
                className="flex w-full items-center gap-4 rounded-xl border border-[#DBEAFE] p-4 text-left transition hover:border-blue-500 hover:bg-blue-50"
              >
                <div className="rounded-lg bg-blue-100 p-2.5 text-[#0052CC]">
                  {role === "Student" ? (
                    <GraduationCap size={18} />
                  ) : role === "Teacher" ? (
                    <ClipboardCheck size={18} />
                  ) : (
                    <ShieldCheck size={18} />
                  )}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-bold text-slate-800">
                    Continue as {role}
                  </p>
                  <p className="mt-1 text-xs text-[#475569]">
                    Explore the {role.toLowerCase()} dashboard
                  </p>
                </div>
                <ChevronRight size={17} className="text-[#475569]" />
              </button>
            ))}
          </div>
          <div className="mt-8 border-t border-[#DBEAFE] pt-6 text-center text-xs text-[#475569]">
            Demo mode · No account required
          </div>
        </div>
      </div>
    </main>
  );
}

function AdminWorkspace({
  students,
  teachers,
  classes,
  reload,
}: {
  students: AdminStudent[];
  teachers: AdminTeacher[];
  classes: AdminClass[];
  reload: () => Promise<void>;
}) {
  const [tab, setTab] = useState<"Students" | "Teachers" | "Classes">(
    "Students",
  );
  const [query, setQuery] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [error, setError] = useState("");
  const [report, setReport] = useState<Record<string, unknown> | null>(null);
  const [editing, setEditing] = useState<{ type: string; id: number } | null>(
    null,
  );
  const filteredStudents = students.filter((item) =>
    `${item.name} ${item.email}`.toLowerCase().includes(query.toLowerCase()),
  );
  const filteredTeachers = teachers.filter((item) =>
    `${item.full_name} ${item.email}`
      .toLowerCase()
      .includes(query.toLowerCase()),
  );
  const filteredClasses = classes.filter((item) =>
    `${item.name} ${item.academic_year}`
      .toLowerCase()
      .includes(query.toLowerCase()),
  );
  const submit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    const data = new FormData(event.currentTarget);
    try {
      if (tab === "Classes")
        await api.createClass({
          name: String(data.get("name")),
          academic_year: String(data.get("academic_year")),
        });
      if (tab === "Students")
        await api.createStudent({
          full_name: String(data.get("full_name")),
          email: String(data.get("email")),
          password: String(data.get("password")),
          phone_number: String(data.get("phone_number")),
          level: String(data.get("level")),
          class_id: Number(data.get("class_id")) || undefined,
        });
      if (tab === "Teachers")
        await api.createTeacher({
          full_name: String(data.get("full_name")),
          email: String(data.get("email")),
          password: String(data.get("password")),
          phone_number: String(data.get("phone_number")),
          class_ids: String(data.get("class_ids") || "")
            .split(",")
            .map(Number)
            .filter(Boolean),
        });
      setFormOpen(false);
      await reload();
    } catch (submissionError) {
      setError(
        submissionError instanceof Error
          ? submissionError.message
          : "Request failed",
      );
    }
  };
  const remove = async (type: string, id: number) => {
    if (!window.confirm("Delete this record?")) return;
    if (type === "student") await api.deleteStudent(id);
    if (type === "teacher") await api.deleteTeacher(id);
    if (type === "class") await api.deleteClass(id);
    await reload();
  };
  return (
    <section className="space-y-7">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-sm text-[#475569]">
            Manage your learning community
          </p>
          <h2 className="mt-1 text-2xl font-bold text-[#0F172A]">
            People & classes
          </h2>
        </div>
        <button
          onClick={() => setFormOpen(true)}
          className="rounded-xl bg-[#0052CC] px-4 py-3 text-xs font-bold text-white"
        >
          <Plus size={15} className="mr-2 inline" />
          Add {tab.slice(0, -1)}
        </button>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <Stat
          label="Total students"
          value={String(students.length)}
          icon={GraduationCap}
        />
        <Stat
          label="Teaching staff"
          value={String(teachers.length)}
          icon={Users}
        />
        <Stat
          label="Active classes"
          value={String(classes.length)}
          icon={BookOpen}
        />
      </div>
      <div className="rounded-2xl border border-[#DBEAFE] bg-white">
        <div className="flex flex-wrap justify-between gap-4 border-b border-[#DBEAFE] p-5">
          <div className="flex gap-1 rounded-lg bg-[#EFF6FF] p-1">
            {(["Students", "Teachers", "Classes"] as const).map((item) => (
              <button
                key={item}
                onClick={() => {
                  setTab(item);
                  setQuery("");
                }}
                className={`rounded-md px-4 py-2 text-xs font-bold ${tab === item ? "bg-white text-[#0052CC] shadow-sm" : "text-[#475569]"}`}
              >
                {item}
              </button>
            ))}
          </div>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={`Search ${tab.toLowerCase()}...`}
            className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-xs"
          />
        </div>
        <div className="divide-y divide-slate-100 p-5">
          {tab === "Students" &&
            (filteredStudents.length ? (
              filteredStudents.map((item) => (
                <div key={item.email} className="flex items-center gap-3 py-3">
                  <Avatar initials={item.initials} />
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-slate-800">
                      {item.name}
                    </p>
                    <p className="text-xs text-[#64748B]">
                      {item.email} · {item.className || "No class"}
                    </p>
                  </div>
                  <button
                    onClick={() =>
                      api
                        .getStudentReport(
                          students.find(
                            (student) => student.email === item.email,
                          )?.student_id ?? 0,
                        )
                        .then(setReport)
                    }
                    className="text-xs font-semibold text-[#0052CC]"
                  >
                    Report
                  </button>
                  <button
                    onClick={() =>
                      remove(
                        "student",
                        students.find((student) => student.email === item.email)
                          ?.student_id ?? 0,
                      )
                    }
                    className="text-xs text-rose-600"
                  >
                    Delete
                  </button>
                </div>
              ))
            ) : (
              <p className="py-5 text-sm text-[#64748B]">No students found.</p>
            ))}
          {tab === "Teachers" &&
            (filteredTeachers.length ? (
              filteredTeachers.map((item) => (
                <div
                  key={item.teacher_id}
                  className="flex items-center gap-3 py-3"
                >
                  <Avatar
                    initials={item.full_name
                      .split(" ")
                      .map((part) => part[0])
                      .join("")
                      .slice(0, 2)}
                  />
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-slate-800">
                      {item.full_name}
                    </p>
                    <p className="text-xs text-[#64748B]">
                      {item.email} · {item.classes.length} classes
                    </p>
                  </div>
                  <button
                    onClick={() => remove("teacher", item.teacher_id)}
                    className="text-xs text-rose-600"
                  >
                    Delete
                  </button>
                </div>
              ))
            ) : (
              <p className="py-5 text-sm text-[#64748B]">No teachers found.</p>
            ))}
          {tab === "Classes" &&
            (filteredClasses.length ? (
              filteredClasses.map((item) => (
                <div
                  key={item.class_id}
                  className="flex items-center gap-3 py-3"
                >
                  <BookOpen className="text-[#0052CC]" size={18} />
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-slate-800">
                      {item.name}
                    </p>
                    <p className="text-xs text-[#64748B]">
                      {item.academic_year}
                    </p>
                  </div>
                  <button
                    onClick={() => remove("class", item.class_id)}
                    className="text-xs text-rose-600"
                  >
                    Delete
                  </button>
                </div>
              ))
            ) : (
              <p className="py-5 text-sm text-[#64748B]">No classes found.</p>
            ))}
        </div>
      </div>
      {formOpen && (
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          <h3 className="font-bold text-[#0F172A]">Add {tab.slice(0, -1)}</h3>
          <form onSubmit={submit} className="mt-4 grid gap-3 sm:grid-cols-2">
            {tab === "Classes" ? (
              <>
                <input
                  name="name"
                  required
                  placeholder="Class name"
                  className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                />
                <input
                  name="academic_year"
                  required
                  placeholder="Academic year"
                  className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                />
              </>
            ) : (
              <>
                <input
                  name="full_name"
                  required
                  placeholder="Full name"
                  className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                />
                <input
                  name="email"
                  required
                  type="email"
                  placeholder="Email"
                  className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                />
                <input
                  name="password"
                  required
                  type="password"
                  placeholder="Password"
                  className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                />
                <input
                  name="phone_number"
                  required
                  placeholder="Phone"
                  className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                />
                {tab === "Students" ? (
                  <input
                    name="level"
                    required
                    placeholder="Level"
                    className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                  />
                ) : (
                  <input
                    name="class_ids"
                    placeholder="Class IDs, comma separated"
                    className="rounded-lg border border-[#DBEAFE] px-3 py-2 text-sm"
                  />
                )}
              </>
            )}
            <button className="rounded-lg bg-[#0052CC] px-4 py-2 text-sm font-bold text-white">
              Save
            </button>
            {error && <p className="text-sm text-rose-600">{error}</p>}
          </form>
        </div>
      )}
      {report && (
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          <div className="flex justify-between">
            <h3 className="font-bold">Academic report</h3>
            <button onClick={() => setReport(null)} className="text-[#0052CC]">
              Close
            </button>
          </div>
          <pre className="mt-3 overflow-auto text-xs">
            {JSON.stringify(report, null, 2)}
          </pre>
        </div>
      )}
    </section>
  );
}

function DynamicStudentWorkspace({
  profile,
  courses,
  exercises,
  grades,
  submissions,
  notifications,
}: {
  profile: ApiStudent;
  courses: Course[];
  exercises: Exercise[];
  grades: Grade[];
  submissions: Submission[];
  notifications: StudentNotification[];
}) {
  const [tab, setTab] = useState("Courses");
  const [feedback, setFeedback] = useState("");
  const submit = async (exerciseId: number) => {
    const filePath = window.prompt("Submission text or file path");
    if (!filePath) return;
    await api.createSubmission({
      exercise_id: exerciseId,
      file_path: filePath,
    });
    setFeedback("Submission sent successfully.");
  };
  return (
    <section className="space-y-7">
      <div>
        <p className="text-sm text-[#64748B]">Student workspace</p>
        <h2 className="mt-1 text-2xl font-bold text-[#0F172A]">
          {profile.full_name}
        </h2>
        <p className="mt-1 text-sm text-[#64748B]">
          {profile.email} · {profile.level ?? "No level"}
        </p>
      </div>
      <div className="flex gap-1 rounded-lg bg-[#EFF6FF] p-1">
        {["Courses", "Grades", "Submissions", "Notifications"].map((item) => (
          <button
            key={item}
            onClick={() => setTab(item)}
            className={`rounded-md px-4 py-2 text-xs font-bold ${tab === item ? "bg-white text-[#0052CC] shadow-sm" : "text-[#475569]"}`}
          >
            {item}
          </button>
        ))}
      </div>
      {feedback && (
        <p className="rounded-lg bg-blue-50 p-3 text-sm text-[#0052CC]">
          {feedback}
        </p>
      )}
      {tab === "Courses" && (
        <div className="grid gap-4 sm:grid-cols-2">
          {courses.length ? (
            courses.map((course) => (
              <div
                key={course.course_id}
                className="rounded-2xl border border-[#DBEAFE] bg-white p-5"
              >
                <h3 className="font-bold text-[#0F172A]">
                  {course.course_name}
                </h3>
                <p className="mt-1 text-xs text-[#64748B]">
                  {course.teacher?.full_name ?? ""} · {course.level}
                </p>
                {exercises
                  .filter(
                    (exercise) =>
                      exercise.course?.course_id === course.course_id,
                  )
                  .map((exercise) => (
                    <div
                      key={exercise.exercise_id}
                      className="mt-4 flex items-center gap-2 border-t border-slate-50 pt-3"
                    >
                      <span className="flex-1 text-sm text-slate-700">
                        {exercise.exercise_name}
                      </span>
                      <button
                        onClick={() => submit(exercise.exercise_id)}
                        className="text-xs font-semibold text-[#0052CC]"
                      >
                        Submit
                      </button>
                    </div>
                  ))}
              </div>
            ))
          ) : (
            <p className="text-sm text-[#64748B]">No courses enrolled.</p>
          )}
        </div>
      )}
      {tab === "Grades" && (
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          {grades.length ? (
            grades.map((grade) => (
              <div
                key={
                  grade.grade_id ?? `${grade.student_id}-${grade.exercise_id}`
                }
                className="flex justify-between border-b border-slate-50 py-3 text-sm"
              >
                <span>Exercise {grade.exercise_id}</span>
                <strong className="text-[#0052CC]">{grade.score}</strong>
              </div>
            ))
          ) : (
            <p className="text-sm text-[#64748B]">No grades available.</p>
          )}
        </div>
      )}
      {tab === "Submissions" && (
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          {submissions.length ? (
            submissions.map((submission) => (
              <div
                key={submission.submission_id}
                className="flex justify-between border-b border-slate-50 py-3 text-sm"
              >
                <span>Exercise {submission.exercise_id}</span>
                <span className="text-[#64748B]">{submission.status}</span>
              </div>
            ))
          ) : (
            <p className="text-sm text-[#64748B]">No submissions yet.</p>
          )}
        </div>
      )}
      {tab === "Notifications" && (
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          {notifications.length ? (
            notifications.map((notification) => (
              <div
                key={notification.notification_id}
                className="border-b border-slate-50 py-3"
              >
                <p className="font-semibold text-slate-800">
                  {notification.title}
                </p>
                <p className="text-xs text-[#64748B]">{notification.message}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-[#64748B]">No new notifications.</p>
          )}
        </div>
      )}
    </section>
  );
}

function ClassicStudentWorkspace({
  active,
  profile,
  courses,
  exercises,
  grades,
  submissions,
  notifications,
}: {
  active: string;
  profile: ApiStudent;
  courses: Course[];
  exercises: Exercise[];
  grades: Grade[];
  submissions: Submission[];
  notifications: StudentNotification[];
}) {
  const [feedback, setFeedback] = useState("");
  const submittedIds = new Set(submissions.map((item) => item.exercise_id));
  const average = grades.length
    ? grades.reduce((sum, item) => sum + item.score, 0) / grades.length
    : 0;
  const progress = exercises.length
    ? Math.round((submittedIds.size / exercises.length) * 100)
    : 0;
  const chartData = exercises.map((exercise) => ({
    name:
      exercise.exercise_name.length > 16
        ? `${exercise.exercise_name.slice(0, 16)}...`
        : exercise.exercise_name,
    score:
      grades.find((grade) => grade.exercise_id === exercise.exercise_id)
        ?.score ?? 0,
  }));
  const announcements = notifications.filter(
    (item) => !item.title.toLowerCase().includes("feedback"),
  );
  const privateFeedback = notifications.filter((item) =>
    item.title.toLowerCase().includes("feedback"),
  );
  const submitExercise = async (exerciseId: number) => {
    const filePath = window.prompt("Enter submission text or file path");
    if (!filePath) return;
    await api.createSubmission({
      exercise_id: exerciseId,
      file_path: filePath,
    });
    setFeedback("Exercise submitted successfully.");
  };

  if (active === "Progress")
    return (
      <section className="space-y-6">
        <div>
          <p className="text-sm text-[#64748B]">Student workspace</p>
          <h2 className="mt-1 text-2xl font-bold text-[#0F172A]">Progress</h2>
        </div>
        <div className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
          <div className="h-[320px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis domain={[0, 20]} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="score" fill="#0052CC" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          {!chartData.length && (
            <p className="text-sm text-[#64748B]">
              No grades or exercises available.
            </p>
          )}
        </div>
      </section>
    );
  if (active === "My Courses")
    return (
      <section className="space-y-5">
        <h2 className="text-2xl font-bold text-[#0F172A]">My Courses</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {courses.length ? (
            courses.map((course) => (
              <div
                key={course.course_id}
                className="rounded-2xl border border-[#DBEAFE] bg-white p-5"
              >
                <h3 className="font-bold text-[#0F172A]">
                  {course.course_name}
                </h3>
                <p className="mt-1 text-xs text-[#64748B]">
                  {course.teacher?.full_name ?? ""} · {course.level ?? ""}
                </p>
                <p className="mt-4 text-sm text-[#475569]">
                  {
                    exercises.filter(
                      (item) => item.course?.course_id === course.course_id,
                    ).length
                  }{" "}
                  exercises
                </p>
              </div>
            ))
          ) : (
            <p className="text-sm text-[#64748B]">No courses enrolled.</p>
          )}
        </div>
      </section>
    );
  if (active === "Announcements")
    return (
      <section className="space-y-5">
        <h2 className="text-2xl font-bold text-[#0F172A]">Announcements</h2>
        <div className="rounded-2xl bg-[#0c2254] p-5 text-white">
          {announcements.length ? (
            announcements.map((item) => (
              <div
                key={item.notification_id}
                className="border-b border-white/10 py-3 last:border-0"
              >
                <h3 className="font-bold">{item.title}</h3>
                <p className="mt-1 text-sm text-blue-100/80">{item.message}</p>
              </div>
            ))
          ) : (
            <p className="text-sm text-blue-100/80">No new announcements.</p>
          )}
        </div>
      </section>
    );
  return (
    <section className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="text-sm text-[#64748B]">Active classroom</p>
          <h2 className="mt-1 text-2xl font-bold text-[#0F172A]">
            {profile.full_name}
          </h2>
          <p className="mt-1 text-sm text-[#64748B]">
            {profile.email} · {profile.level ?? "No level"}
          </p>
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Stat
          label="Average score"
          value={grades.length ? `${average.toFixed(1)} / 20` : "-"}
          icon={BarChart3}
        />
        <Stat
          label="Exercises done"
          value={`${submittedIds.size} / ${exercises.length}`}
          icon={ClipboardCheck}
        />
        <Stat
          label="Overall progress"
          value={`${progress}%`}
          icon={GraduationCap}
        />
      </div>
      {feedback && (
        <p className="rounded-lg bg-blue-50 p-3 text-sm text-[#0052CC]">
          {feedback}
        </p>
      )}
      <div className="grid gap-5 xl:grid-cols-[1.6fr_1fr]">
        <section className="rounded-2xl border border-[#DBEAFE] bg-white">
          <div className="border-b border-[#DBEAFE] px-5 py-4">
            <h2 className="font-bold text-[#0F172A]">Learning path</h2>
            <p className="mt-1 text-xs text-[#475569]">
              Courses and exercises for your class
            </p>
          </div>
          <div className="space-y-3 p-5">
            {courses.length ? (
              courses.map((course) => (
                <div
                  key={course.course_id}
                  className="rounded-xl border border-[#DBEAFE]"
                >
                  <div className="flex items-center gap-3 px-4 py-3">
                    <BookOpen className="text-[#0052CC]" size={17} />
                    <div>
                      <h3 className="text-sm font-semibold text-slate-800">
                        {course.course_name}
                      </h3>
                      <p className="text-[11px] text-[#475569]">
                        with {course.teacher?.full_name ?? ""}
                      </p>
                    </div>
                  </div>
                  {exercises
                    .filter(
                      (item) => item.course?.course_id === course.course_id,
                    )
                    .map((exercise) => (
                      <div
                        key={exercise.exercise_id}
                        className="flex items-center gap-3 border-t border-[#DBEAFE] px-4 py-3"
                      >
                        <span
                          className={`h-2 w-2 rounded-full ${submittedIds.has(exercise.exercise_id) ? "bg-emerald-500" : "bg-slate-300"}`}
                        />
                        <span className="flex-1 text-xs font-medium text-slate-700">
                          {exercise.exercise_name}
                        </span>
                        <span className="rounded-full bg-[#EFF6FF] px-2 py-1 text-[10px] font-semibold text-[#475569]">
                          {submittedIds.has(exercise.exercise_id)
                            ? "Submitted"
                            : "Not submitted"}
                        </span>
                        {!submittedIds.has(exercise.exercise_id) && (
                          <button
                            onClick={() => submitExercise(exercise.exercise_id)}
                            className="text-xs font-bold text-[#0052CC]"
                          >
                            Submit
                          </button>
                        )}
                        <span className="w-14 text-right text-xs font-bold">
                          {grades.find(
                            (grade) =>
                              grade.exercise_id === exercise.exercise_id,
                          )?.score ?? "-"}
                        </span>
                      </div>
                    ))}
                </div>
              ))
            ) : (
              <p className="text-sm text-[#64748B]">No courses enrolled.</p>
            )}
          </div>
        </section>
        <aside className="space-y-5">
          <section className="rounded-2xl bg-[#0c2254] p-5 text-white">
            <div className="flex items-center gap-2 text-blue-200">
              <Bell size={16} />
              <span className="text-xs font-semibold uppercase tracking-[.15em]">
                Announcements
              </span>
            </div>
            {announcements.length ? (
              announcements.slice(0, 3).map((item) => (
                <div key={item.notification_id} className="mt-4">
                  <h3 className="font-bold">{item.title}</h3>
                  <p className="mt-1 text-sm text-blue-100/80">
                    {item.message}
                  </p>
                </div>
              ))
            ) : (
              <p className="mt-4 text-sm text-blue-100/80">
                No new announcements.
              </p>
            )}
          </section>
          <section className="rounded-2xl border border-[#DBEAFE] bg-white p-5">
            <h2 className="font-bold text-[#0F172A]">Recent feedback</h2>
            {privateFeedback.length ? (
              privateFeedback.slice(0, 3).map((item) => (
                <div
                  key={item.notification_id}
                  className="mt-4 border-b border-slate-50 pb-3"
                >
                  <p className="text-xs font-semibold text-slate-800">
                    {item.title}
                  </p>
                  <p className="mt-1 text-xs leading-5 text-[#475569]">
                    {item.message}
                  </p>
                </div>
              ))
            ) : (
              <p className="mt-4 text-sm text-[#64748B]">
                No private feedback yet.
              </p>
            )}
          </section>
        </aside>
      </div>
    </section>
  );
}

function ConnectedApp() {
  const [role, setRole] = useState<Role | null>(null);
  const [userName, setUserName] = useState("User");
  const [adminStudents, setAdminStudents] = useState<AdminStudent[]>([]);
  const [adminTeachers, setAdminTeachers] = useState<AdminTeacher[]>([]);
  const [adminClasses, setAdminClasses] = useState<AdminClass[]>([]);
  const [teacherData, setTeacherData] = useState<Teacher | null>(null);
  const [teacherStudents, setTeacherStudents] = useState<AttendanceStudent[]>(
    [],
  );
  const [teacherCourses, setTeacherCourses] = useState<TeacherCourse[]>([]);
  const [teacherExercises, setTeacherExercises] = useState<TeacherExercise[]>(
    [],
  );
  const [teacherGrades, setTeacherGrades] = useState<Grade[]>([]);
  const [teacherAttendance, setTeacherAttendance] = useState<
    AttendanceRecord[]
  >([]);
  const [teacherNotifications, setTeacherNotifications] = useState<
    TeacherNotification[]
  >([]);
  const [studentProfile, setStudentProfile] = useState<ApiStudent | null>(null);
  const [studentCourses, setStudentCourses] = useState<Course[]>([]);
  const [studentExercises, setStudentExercises] = useState<Exercise[]>([]);
  const [studentGrades, setStudentGrades] = useState<Grade[]>([]);
  const [studentSubmissions, setStudentSubmissions] = useState<Submission[]>(
    [],
  );
  const [studentNotifications, setStudentNotifications] = useState<
    StudentNotification[]
  >([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [active, setActive] = useState("Overview");
  const reloadAdmin = async () => {
    const [apiStudents, apiTeachers, apiClasses] = await Promise.all([
      api.getStudents(),
      api.getTeachers(),
      api.getClasses(),
    ]);
    setAdminStudents(
      apiStudents.map((student) => ({
        name: student.full_name,
        email: student.email,
        className: student.level ?? "",
        status: "Active",
        initials: student.full_name
          .split(" ")
          .map((part) => part[0])
          .join("")
          .slice(0, 2)
          .toUpperCase(),
      })),
    );
    setAdminTeachers(apiTeachers);
    setAdminClasses(apiClasses);
  };

  useEffect(() => {
    let cancelled = false;
    const session = api.getSession();
    const sessionRole = session.role;
    if (!session.token || !sessionRole)
      return () => {
        cancelled = true;
      };
    const requiredRole =
      window.location.pathname === "/admin"
        ? "admin"
        : window.location.pathname === "/teacher"
          ? "teacher"
          : window.location.pathname === "/student"
            ? "student"
            : null;
    if (requiredRole && requiredRole !== sessionRole) {
      window.location.replace(`/${sessionRole}`);
      return () => {
        cancelled = true;
      };
    }
    const displayRole = (sessionRole[0].toUpperCase() +
      sessionRole.slice(1)) as Role;
    if (!cancelled) setRole(displayRole);

    const loadData = async () => {
      if (sessionRole === "admin") {
        const [profile, apiStudents, apiTeachers, apiClasses] =
          await Promise.all([
            api.getAdminProfile(),
            api.getStudents(),
            api.getTeachers(),
            api.getClasses(),
          ]);
        if (!cancelled) {
          setUserName(profile.full_name);
          setAdminStudents(
            apiStudents.map((student) => ({
              name: student.full_name,
              email: student.email,
              className: student.level ?? "",
              status: "Active",
              initials: student.full_name
                .split(" ")
                .map((part) => part[0])
                .join("")
                .slice(0, 2)
                .toUpperCase(),
            })),
          );
          setAdminTeachers(apiTeachers);
          setAdminClasses(apiClasses);
        }
        students = apiStudents.map((student) => ({
          name: student.full_name,
          email: student.email,
          className: student.level ?? "",
          status: "Active",
          initials: student.full_name
            .split(" ")
            .map((part) => part[0])
            .join("")
            .slice(0, 2)
            .toUpperCase(),
        }));
      }
      if (sessionRole === "teacher") {
        const teacher = await api.getTeacher();
        const [
          classStudentGroups,
          apiCourses,
          apiExercises,
          apiGrades,
          apiAttendance,
          allNotifications,
        ] = await Promise.all([
          Promise.all(
            teacher.classes.map((item) =>
              api.getAttendanceStudents(item.class_id),
            ),
          ),
          api.getTeacherCourses(),
          api.getTeacherExercises(),
          api.getTeacherGrades(),
          api.getTeacherAttendance(),
          api.getNotifications(),
        ]);
        if (!cancelled) {
          setUserName(teacher.full_name);
          setTeacherData(teacher);
          setTeacherStudents(classStudentGroups.flat());
          setTeacherCourses(apiCourses);
          setTeacherExercises(apiExercises);
          setTeacherGrades(apiGrades);
          setTeacherAttendance(apiAttendance);
          setTeacherNotifications(
            allNotifications.filter(
              (item) => item.teacher_id === teacher.teacher_id,
            ),
          );
        }
      }
      if (sessionRole === "student") {
        const [
          profile,
          apiCourses,
          apiExercises,
          apiGrades,
          apiSubmissions,
          apiNotifications,
        ] = await Promise.all([
          api.getStudentProfile(),
          api.getStudentCourses(),
          api.getStudentExercises(),
          api.getStudentGrades(),
          api.getStudentSubmissions(),
          api.getStudentNotifications(),
        ]);
        if (!cancelled) {
          setUserName(profile.full_name);
          setStudentProfile(profile);
          setStudentCourses(apiCourses);
          setStudentExercises(apiExercises);
          setStudentGrades(apiGrades);
          setStudentSubmissions(apiSubmissions);
          setStudentNotifications(apiNotifications);
        }
        courses = apiCourses.map((course) => ({
          name: course.course_name,
          teacher: course.teacher?.full_name ?? "",
          exercises: apiExercises
            .filter(
              (exercise) => exercise.course?.course_id === course.course_id,
            )
            .map((exercise) => {
              const grade = apiGrades.find(
                (item) => item.exercise_id === exercise.exercise_id,
              );
              return {
                name: exercise.exercise_name,
                score: grade ? String(grade.score) : "—",
                state: grade ? "Submitted" : "Not submitted",
              };
            }),
        }));
      }
    };
    loadData().catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, []);

  if (!role) return <Login setRole={setRole} />;
  const logout = () => {
    api.logout();
    window.location.assign("/login");
  };
  return (
    <div className="flex min-h-screen bg-white text-[#0F172A]">
      <Sidebar
        role={role}
        open={sidebarOpen}
        setOpen={setSidebarOpen}
        active={active}
        userName={userName}
        onLogout={logout}
        setActive={setActive}
      />
      <div className="min-w-0 flex-1">
        <Topbar
          role={role}
          setOpen={setSidebarOpen}
          onLogout={logout}
          userName={userName}
          notifications={teacherNotifications}
        />
        <main className="mx-auto max-w-[1500px] p-5 md:p-8">
          {role === "Student" ? (
            studentProfile ? (
              <ClassicStudentWorkspace
                active={active}
                profile={studentProfile}
                courses={studentCourses}
                exercises={studentExercises}
                grades={studentGrades}
                submissions={studentSubmissions}
                notifications={studentNotifications}
              />
            ) : (
              <p className="text-sm text-[#64748B]">
                Loading student workspace...
              </p>
            )
          ) : role === "Teacher" ? (
            teacherData ? (
              <DynamicTeacherWorkspace
                active={active}
                teacher={teacherData}
                students={teacherStudents}
                courses={teacherCourses}
                exercises={teacherExercises}
                grades={teacherGrades}
                attendance={teacherAttendance}
                onAttendanceSaved={async () => {
                  if (teacherData)
                    setTeacherAttendance(await api.getTeacherAttendance());
                }}
              />
            ) : (
              <p className="text-sm text-[#64748B]">
                Loading teacher workspace...
              </p>
            )
          ) : (
            <AdminWorkspace
              students={adminStudents}
              teachers={adminTeachers}
              classes={adminClasses}
              reload={reloadAdmin}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default function Home() {
  return <ConnectedApp />;
}
