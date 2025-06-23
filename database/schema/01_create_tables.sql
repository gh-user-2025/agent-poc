-- ======================================================================
-- 工場設備管理システム データベーススキーマ作成スクリプト
-- Azure SQL Database v12 対応
-- ======================================================================

-- 設備マスタテーブル
CREATE TABLE Equipment (
    EquipmentId INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentName NVARCHAR(100) NOT NULL,
    EquipmentType NVARCHAR(50) NOT NULL,
    Location NVARCHAR(100) NOT NULL,
    InstallationDate DATE NOT NULL,
    Manufacturer NVARCHAR(100),
    ModelNumber NVARCHAR(50),
    MaxOperatingHours INT,
    MaintenanceCycle INT, -- メンテナンス周期（日数）
    Status NVARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Inactive', 'Maintenance', 'Retired')),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE()
);

-- メンテナンス履歴テーブル
CREATE TABLE MaintenanceHistory (
    MaintenanceId INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentId INT NOT NULL,
    MaintenanceType NVARCHAR(50) NOT NULL,
    PerformedDate DATETIME2 NOT NULL,
    Technician NVARCHAR(100) NOT NULL,
    WorkDescription NVARCHAR(MAX),
    PartsReplaced NVARCHAR(MAX),
    Cost DECIMAL(10,2),
    NextScheduledDate DATE,
    Status NVARCHAR(20) DEFAULT 'Completed' CHECK (Status IN ('Scheduled', 'InProgress', 'Completed', 'Cancelled')),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (EquipmentId) REFERENCES Equipment(EquipmentId)
);

-- 部品マスタテーブル
CREATE TABLE Parts (
    PartId INT IDENTITY(1,1) PRIMARY KEY,
    PartName NVARCHAR(100) NOT NULL,
    PartNumber NVARCHAR(50) NOT NULL UNIQUE,
    Supplier NVARCHAR(100),
    UnitPrice DECIMAL(10,2),
    StockQuantity INT DEFAULT 0,
    MinimumStock INT DEFAULT 0,
    Category NVARCHAR(50),
    Description NVARCHAR(500),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE()
);

-- 設備-部品関連テーブル
CREATE TABLE EquipmentParts (
    EquipmentId INT NOT NULL,
    PartId INT NOT NULL,
    Quantity INT DEFAULT 1,
    PRIMARY KEY (EquipmentId, PartId),
    FOREIGN KEY (EquipmentId) REFERENCES Equipment(EquipmentId),
    FOREIGN KEY (PartId) REFERENCES Parts(PartId)
);

-- センサーマスタテーブル（SQL Database側でマスタ管理）
CREATE TABLE Sensors (
    SensorId INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentId INT NOT NULL,
    SensorType NVARCHAR(50) NOT NULL, -- 'temperature', 'pressure', 'vibration', 'current', 'humidity'
    SensorName NVARCHAR(100) NOT NULL,
    MeasurementUnit NVARCHAR(20) NOT NULL,
    MinThreshold DECIMAL(10,3),
    MaxThreshold DECIMAL(10,3),
    Status NVARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Inactive', 'Maintenance')),
    InstallationDate DATE,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (EquipmentId) REFERENCES Equipment(EquipmentId)
);

-- ユーザーマスタテーブル
CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    FullName NVARCHAR(100) NOT NULL,
    Role NVARCHAR(30) NOT NULL CHECK (Role IN ('Administrator', 'Operator', 'Technician', 'Viewer')),
    Department NVARCHAR(50),
    Status NVARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Inactive')),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE()
);

-- メンテナンススケジュールテーブル
CREATE TABLE MaintenanceSchedule (
    ScheduleId INT IDENTITY(1,1) PRIMARY KEY,
    EquipmentId INT NOT NULL,
    ScheduledDate DATE NOT NULL,
    MaintenanceType NVARCHAR(50) NOT NULL,
    AssignedTechnician INT,
    EstimatedDuration INT, -- 予想所要時間（分）
    Priority NVARCHAR(20) DEFAULT 'Medium' CHECK (Priority IN ('Low', 'Medium', 'High', 'Critical')),
    Status NVARCHAR(20) DEFAULT 'Scheduled' CHECK (Status IN ('Scheduled', 'InProgress', 'Completed', 'Cancelled')),
    Notes NVARCHAR(500),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (EquipmentId) REFERENCES Equipment(EquipmentId),
    FOREIGN KEY (AssignedTechnician) REFERENCES Users(UserId)
);

-- インデックスの作成
CREATE INDEX IX_Equipment_Type ON Equipment(EquipmentType);
CREATE INDEX IX_Equipment_Location ON Equipment(Location);
CREATE INDEX IX_Equipment_Status ON Equipment(Status);
CREATE INDEX IX_MaintenanceHistory_EquipmentId ON MaintenanceHistory(EquipmentId);
CREATE INDEX IX_MaintenanceHistory_PerformedDate ON MaintenanceHistory(PerformedDate);
CREATE INDEX IX_Parts_PartNumber ON Parts(PartNumber);
CREATE INDEX IX_Parts_Category ON Parts(Category);
CREATE INDEX IX_Sensors_EquipmentId ON Sensors(EquipmentId);
CREATE INDEX IX_Sensors_Type ON Sensors(SensorType);
CREATE INDEX IX_MaintenanceSchedule_EquipmentId ON MaintenanceSchedule(EquipmentId);
CREATE INDEX IX_MaintenanceSchedule_ScheduledDate ON MaintenanceSchedule(ScheduledDate);
CREATE INDEX IX_Users_Role ON Users(Role);
CREATE INDEX IX_Users_Department ON Users(Department);

-- データ更新時のタイムスタンプ自動更新用トリガー
CREATE TRIGGER TR_Equipment_UpdateTimestamp
ON Equipment
AFTER UPDATE
AS
BEGIN
    UPDATE Equipment 
    SET UpdatedAt = GETDATE() 
    WHERE EquipmentId IN (SELECT EquipmentId FROM inserted);
END;

CREATE TRIGGER TR_Parts_UpdateTimestamp
ON Parts
AFTER UPDATE
AS
BEGIN
    UPDATE Parts 
    SET UpdatedAt = GETDATE() 
    WHERE PartId IN (SELECT PartId FROM inserted);
END;

CREATE TRIGGER TR_Sensors_UpdateTimestamp
ON Sensors
AFTER UPDATE
AS
BEGIN
    UPDATE Sensors 
    SET UpdatedAt = GETDATE() 
    WHERE SensorId IN (SELECT SensorId FROM inserted);
END;

CREATE TRIGGER TR_Users_UpdateTimestamp
ON Users
AFTER UPDATE
AS
BEGIN
    UPDATE Users 
    SET UpdatedAt = GETDATE() 
    WHERE UserId IN (SELECT UserId FROM inserted);
END;

CREATE TRIGGER TR_MaintenanceSchedule_UpdateTimestamp
ON MaintenanceSchedule
AFTER UPDATE
AS
BEGIN
    UPDATE MaintenanceSchedule 
    SET UpdatedAt = GETDATE() 
    WHERE ScheduleId IN (SELECT ScheduleId FROM inserted);
END;